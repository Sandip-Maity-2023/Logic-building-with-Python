from pathlib import Path

import numpy as np
import tensorflow as tf

from inference_utils import load_and_prepare_image, validate_fundus_image


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = BASE_DIR / "eye_disease_model.keras"
DEFAULT_CLASS_NAMES_PATH = BASE_DIR / "class_names.npy"


def predict_new_image(
    image_path,
    model_path=DEFAULT_MODEL_PATH,
    class_names_path=DEFAULT_CLASS_NAMES_PATH,
):
    """Load the saved model and predict the eye disease in a new image."""
    image_path = Path(image_path)
    model_path = Path(model_path)
    class_names_path = Path(class_names_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not class_names_path.exists():
        raise FileNotFoundError(f"Class names file not found: {class_names_path}")

    loaded_model = tf.keras.models.load_model(model_path)
    loaded_classes = np.load(class_names_path, allow_pickle=True).tolist()

    img_array = load_and_prepare_image(image_path)
    validate_fundus_image(img_array, image_path)
    img_array = tf.expand_dims(img_array, axis=0)

    logits = loaded_model.predict(img_array, verbose=0)
    probabilities = tf.nn.softmax(logits[0]).numpy()
    pred_index = int(np.argmax(probabilities))

    label = loaded_classes[pred_index]
    confidence = float(probabilities[pred_index])
    return label, confidence


if __name__ == "__main__":
    sample_image = BASE_DIR / "t2.jpeg"
    label, confidence = predict_new_image(sample_image)
    print("Prediction:", label)
    print("Confidence:", confidence)
