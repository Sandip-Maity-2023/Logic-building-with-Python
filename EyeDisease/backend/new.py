from pathlib import Path
import copy
import os

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report
from torch.utils.data import DataLoader, Subset, random_split
from torchvision import datasets, models, transforms
from tqdm import tqdm


BASE_DIR = Path(__file__).resolve().parent
DATASET_CANDIDATES = [BASE_DIR / "datasets", BASE_DIR / "dataset"]
BATCH_SIZE = 32
EPOCHS = 20
LR = 1e-4
IMG_SIZE = 256
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH = BASE_DIR / "odir_best.pth"
SPLIT_SEED = 42
NUM_WORKERS = min(4, os.cpu_count() or 0)


def resolve_dataset_path():
    for candidate in DATASET_CANDIDATES:
        if candidate.exists() and any(path.is_dir() for path in candidate.iterdir()):
            return candidate
    raise FileNotFoundError(
        f"No valid dataset directory found. Checked: {', '.join(str(path) for path in DATASET_CANDIDATES)}"
    )


train_transform = transforms.Compose(
    [
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomRotation(15),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

val_transform = transforms.Compose(
    [
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def build_dataloaders(dataset_path):
    base_dataset = datasets.ImageFolder(str(dataset_path))
    class_names = base_dataset.classes
    num_classes = len(class_names)

    print("Dataset Path:", dataset_path)
    print("Classes:", class_names)

    train_size = int(0.7 * len(base_dataset))
    val_size = int(0.15 * len(base_dataset))
    test_size = len(base_dataset) - train_size - val_size

    generator = torch.Generator().manual_seed(SPLIT_SEED)
    train_indices, val_indices, test_indices = random_split(
        range(len(base_dataset)),
        [train_size, val_size, test_size],
        generator=generator,
    )

    train_dataset = copy.copy(base_dataset)
    val_dataset = copy.copy(base_dataset)
    test_dataset = copy.copy(base_dataset)

    train_dataset.transform = train_transform
    val_dataset.transform = val_transform
    test_dataset.transform = val_transform

    train_ds = Subset(train_dataset, train_indices.indices)
    val_ds = Subset(val_dataset, val_indices.indices)
    test_ds = Subset(test_dataset, test_indices.indices)

    train_loader = DataLoader(
        train_ds,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=(DEVICE == "cuda"),
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(DEVICE == "cuda"),
    )
    test_loader = DataLoader(
        test_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(DEVICE == "cuda"),
    )

    targets = np.array(base_dataset.targets)
    class_counts = np.bincount(targets, minlength=num_classes)
    class_weights = 1.0 / np.maximum(class_counts, 1)
    class_weights = torch.tensor(class_weights, dtype=torch.float32, device=DEVICE)

    return train_loader, val_loader, test_loader, class_names, num_classes, class_weights


class HybridModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        weights = models.MobileNet_V3_Small_Weights.DEFAULT
        backbone = models.mobilenet_v3_small(weights=weights)
        self.backbone = backbone.features
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.projection = nn.Linear(576, 576)

        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=576,
                nhead=8,
                batch_first=True,
            ),
            num_layers=4,
        )

        self.fc = nn.Linear(576, num_classes)

    def forward(self, x):
        feat = self.backbone(x)
        batch_size, channels, height, width = feat.shape
        feat = feat.flatten(2).transpose(1, 2)
        feat = self.projection(feat)
        out = self.transformer(feat)
        out = out.mean(dim=1)
        return self.fc(out)


def train_epoch(model, train_loader, criterion, optimizer):
    model.train()
    total_loss = 0.0

    for images, labels in tqdm(train_loader, desc="Training", leave=False):
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / max(len(train_loader), 1)


def evaluate(model, data_loader, class_names):
    model.eval()
    preds = []
    targets = []

    with torch.no_grad():
        for images, labels in data_loader:
            images = images.to(DEVICE)
            outputs = model(images)
            predicted = outputs.argmax(dim=1)

            preds.extend(predicted.cpu().numpy())
            targets.extend(labels.numpy())

    return classification_report(
        targets,
        preds,
        labels=list(range(len(class_names))),
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )


def main():
    dataset_path = resolve_dataset_path()
    train_loader, val_loader, test_loader, class_names, num_classes, class_weights = build_dataloaders(
        dataset_path
    )

    model = HybridModel(num_classes).to(DEVICE)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)

    best_f1 = 0.0

    for epoch in range(1, EPOCHS + 1):
        loss = train_epoch(model, train_loader, criterion, optimizer)
        metrics = evaluate(model, val_loader, class_names)
        f1 = metrics["weighted avg"]["f1-score"]
        scheduler.step()

        print(f"\nEpoch {epoch}/{EPOCHS}")
        print("Loss:", loss)
        print("Validation F1:", f1)

        if f1 > best_f1:
            best_f1 = f1
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"Model saved -> {MODEL_PATH}")

    test_metrics = evaluate(model, test_loader, class_names)
    print("\nTraining complete")
    print("Best Validation F1:", best_f1)
    print("Test Accuracy:", test_metrics["accuracy"])
    print("Test Weighted F1:", test_metrics["weighted avg"]["f1-score"])


if __name__ == "__main__":
    main()
