from __future__ import annotations

import random
import warnings
from pathlib import Path

from PIL import Image

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "archive" / "dataset"
IMAGE_SIZE = (256, 256)
TRAIN_BATCH_SIZE = 24
VAL_BATCH_SIZE = 32
SEED = 123


def get_tf():
    try:
        import tensorflow as tf
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "TensorFlow is required to train the eye model. Install it in the backend environment first."
        ) from exc

    return tf


def get_class_directories(dataset_dir: Path) -> list[Path]:
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    class_dirs = sorted(path for path in dataset_dir.iterdir() if path.is_dir())
    if not class_dirs:
        raise ValueError(f"No class folders were found in: {dataset_dir}")

    return class_dirs


def load_datasets(dataset_dir: Path):
    tf = get_tf()

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="training",
        batch_size=TRAIN_BATCH_SIZE,
        image_size=IMAGE_SIZE,
        seed=SEED,
        shuffle=True,
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="validation",
        batch_size=VAL_BATCH_SIZE,
        image_size=IMAGE_SIZE,
        seed=SEED,
        shuffle=True,
    )

    return train_ds, val_ds


def visualize_images(path: Path, target_size: tuple[int, int] = IMAGE_SIZE, num_images: int = 5):
    import matplotlib.pyplot as plt

    image_files = [file for file in path.iterdir() if file.is_file()]
    if not image_files:
        raise ValueError(f"No images found in: {path}")

    selected_images = random.sample(image_files, min(num_images, len(image_files)))
    fig, axes = plt.subplots(1, len(selected_images), figsize=(15, 3), facecolor="white")

    if len(selected_images) == 1:
        axes = [axes]

    for axis, image_path in zip(axes, selected_images):
        image = Image.open(image_path).resize(target_size)
        axis.imshow(image)
        axis.axis("off")
        axis.set_title(image_path.name)

    plt.tight_layout()
    plt.show()


def build_model(num_classes: int):
    tf = get_tf()

    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.2),
        ]
    )

    base_model = tf.keras.applications.MobileNetV2(
        include_top=False,
        weights="imagenet",
        input_shape=(*IMAGE_SIZE, 3),
    )
    base_model.trainable = False

    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3))
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(num_classes)(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    return model, base_model


def plot_history(history):
    import matplotlib.pyplot as plt

    plt.plot(history.history["accuracy"], label="Training Accuracy", marker="o")
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy", marker="o")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.legend()
    plt.show()

    plt.plot(history.history["loss"], label="Training Loss", marker="o")
    plt.plot(history.history["val_loss"], label="Validation Loss", marker="o")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.show()


def train_model(dataset_dir: Path = DATASET_DIR, epochs: int = 25, show_samples: bool = False):
    tf = get_tf()
    keras_callbacks = tf.keras.callbacks

    class_dirs = get_class_directories(dataset_dir)
    class_names = [path.name for path in class_dirs]

    print("Class Names:", class_names)
    print("Number of Classes:", len(class_names))

    if show_samples:
        for class_dir in class_dirs:
            visualize_images(class_dir, num_images=5)

    train_ds, val_ds = load_datasets(dataset_dir)

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=autotune)
    val_ds = val_ds.cache().prefetch(buffer_size=autotune)

    model, base_model = build_model(len(class_names))
    base_model.summary()

    early_stopping = keras_callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
    )

    history = model.fit(
        train_ds,
        epochs=epochs,
        validation_data=val_ds,
        callbacks=[early_stopping],
    )

    plot_history(history)
    return model, history, class_names


def main():
    train_model()


if __name__ == "__main__":
    main()
