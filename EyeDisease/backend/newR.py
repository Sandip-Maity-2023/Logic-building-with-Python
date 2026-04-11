import torch
from PIL import Image
from torchvision import transforms

from train_odir import HybridModel, class_names

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = HybridModel(len(class_names))
model.load_state_dict(torch.load("odir_best.pth"))
model.to(DEVICE)
model.eval()

transform = transforms.Compose([
    transforms.Resize((256,256)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485,0.456,0.406],
        [0.229,0.224,0.225]
    )
])

def predict(image_path):

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(image)
        pred = output.argmax(1).item()

    return class_names[pred]

print(predict("EyeDisease\\backend\\t2.jpeg"))