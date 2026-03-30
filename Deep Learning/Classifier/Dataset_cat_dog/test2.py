from pathlib import Path

import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

BASE_DIR = Path.cwd()
if not (BASE_DIR / "Classifier").exists():
    BASE_DIR = BASE_DIR / "Deep Learning"
model_path = BASE_DIR / "resnet50_cat_dog.h5"
img_path = BASE_DIR / "Classifier" / "Dataset_cat_dog" / "test" / "cats" / "cat_18.jpg"

if not model_path.exists():
    raise FileNotFoundError(f"Model file not found: {model_path}")

if not img_path.exists():
    raise FileNotFoundError(f"Image file not found: {img_path}")

model = load_model(str(model_path))

img = image.load_img(str(img_path), target_size=(224,224))
img = image.img_to_array(img)/255.0
img = np.expand_dims(img, axis=0)

pred = model.predict(img, verbose=0)

if pred[0][0] > 0.5:
    print("Dog")
else:
    print("Cat")