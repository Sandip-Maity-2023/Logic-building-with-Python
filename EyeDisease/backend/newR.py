from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from model_def import HybridModel


BASE_DIR = Path(__file__).resolve().parent
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH = BASE_DIR / "odir_best.pth"
CLASS_NAMES_PATH = BASE_DIR / "class_names.npy"
DATASET_CANDIDATES = [BASE_DIR / "datasets", BASE_DIR / "dataset"]


def load_class_names(expected_count):
    if CLASS_NAMES_PATH.exists():
        saved_class_names = np.load(CLASS_NAMES_PATH, allow_pickle=True).tolist()
        if len(saved_class_names) == expected_count:
            return saved_class_names

    for dataset_dir in DATASET_CANDIDATES:
        if dataset_dir.exists():
            folder_names = sorted(path.name for path in dataset_dir.iterdir() if path.is_dir())
            if len(folder_names) == expected_count:
                return folder_names

    raise ValueError(
        f"Could not find {expected_count} class names that match the checkpoint. "
        f"Checked {CLASS_NAMES_PATH} and dataset folders."
    )


state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
num_classes = state_dict["fc.weight"].shape[0]
class_names = load_class_names(num_classes)

model = HybridModel(len(class_names))
model.load_state_dict(state_dict)
model.to(DEVICE)
model.eval()

transform = transforms.Compose(
    [
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


def _predict_tensor(image):
    image = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(image)
        probabilities = torch.softmax(output, dim=1)[0].cpu().numpy()

    return probabilities


def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    probabilities = _predict_tensor(image)
    pred = int(np.argmax(probabilities))
    return class_names[pred]


def predict_with_confidence(image):
    if isinstance(image, (str, Path)):
        pil_image = Image.open(image).convert("RGB")
    else:
        pil_image = image.convert("RGB")

    probabilities = _predict_tensor(pil_image)
    pred = int(np.argmax(probabilities))

    return {
        "label": class_names[pred],
        "confidence": float(probabilities[pred]),
        "probabilities": {
            class_name: float(score) for class_name, score in zip(class_names, probabilities)
        },
    }


if __name__ == "__main__":
    print(predict(BASE_DIR / "t2.jpeg"))
