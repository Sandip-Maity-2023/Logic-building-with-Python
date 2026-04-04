from pathlib import Path

import numpy as np
import tensorflow as tf

from inference_utils import load_and_prepare_image, validate_fundus_image


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CLASS_NAMES = ["cataract", "diabetic_retinopathy", "glaucoma", "normal"]
MODEL_CANDIDATES = [
    BASE_DIR / "eye_disease_mobilenet.h5",
]
CLASS_NAMES_CANDIDATES = [
    BASE_DIR / "class_names.npy",
]


def find_existing_path(candidates):
    for candidate in candidates:
        if Path(candidate).exists():
            return Path(candidate)
    return None


def load_class_names():
    class_names_path = find_existing_path(CLASS_NAMES_CANDIDATES)
    if class_names_path is None:
        return DEFAULT_CLASS_NAMES
    return np.load(class_names_path, allow_pickle=True).tolist()


def load_prediction_model(model_path=None):
    if model_path is not None:
        resolved_model_path = Path(model_path)
    else:
        resolved_model_path = find_existing_path(MODEL_CANDIDATES)

    if resolved_model_path is None:
        searched_paths = "\n".join(str(path) for path in MODEL_CANDIDATES)
        raise FileNotFoundError(
            "Model file not found. Searched these locations:\n"
            f"{searched_paths}\n"
            "Train and save the model first using model2.py."
        )

    return tf.keras.models.load_model(resolved_model_path)


def predict_image(img_path, model=None):
    img_path = Path(img_path)
    if not img_path.exists():
        raise FileNotFoundError(f"Image file not found: {img_path}")

    if model is None:
        model = load_prediction_model()

    img_array = load_and_prepare_image(img_path)
    validate_fundus_image(img_array, img_path)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)
    raw_scores = predictions[0]

    if np.all(raw_scores >= 0) and np.all(raw_scores <= 1) and np.isclose(np.sum(raw_scores), 1.0, atol=1e-3):
        probabilities = raw_scores
    else:
        probabilities = tf.nn.softmax(raw_scores).numpy()

    class_id = int(np.argmax(probabilities))
    confidence = float(np.max(probabilities))
    class_names = load_class_names()

    return class_names[class_id], confidence


if __name__ == "__main__":
    sample_image = r"EyeDisease\backend\t8.jpeg"
    predicted_class, confidence = predict_image(sample_image)
    print("Prediction:", predicted_class)
    print("Confidence:", confidence)
