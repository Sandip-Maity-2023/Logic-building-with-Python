from pathlib import Path

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "vgg16_cat_dog.h5"
IMAGE_PATH = BASE_DIR / "test" / "cats" / "cat_1.jpg"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

if not IMAGE_PATH.exists():
    raise FileNotFoundError(f"Test image not found: {IMAGE_PATH}")

model = load_model(str(MODEL_PATH))

img = image.load_img(str(IMAGE_PATH), target_size=(224, 224))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

prediction = model.predict(img_array, verbose=0)
label = "Dog" if prediction[0][0] > 0.5 else "Cat"

print(f"Prediction: {label}")
