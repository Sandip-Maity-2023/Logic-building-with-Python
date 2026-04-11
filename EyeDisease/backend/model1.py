from pathlib import Path
import random
import warnings

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras import callbacks


warnings.filterwarnings("ignore")


BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
MODEL_SAVE_PATH = BASE_DIR / "eye_disease_model.keras"
SAVED_MODEL_DIR = BASE_DIR / "eye_disease_savedmodel"
CLASS_NAMES_PATH = BASE_DIR / "class_names.npy"
TRAINING_PLOT_PATH = BASE_DIR / "training_history.png"

IMAGE_SIZE = (256, 256)
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
SEED = 42


def get_class_names(dataset_dir):
    return sorted([path.name for path in dataset_dir.iterdir() if path.is_dir()])


def visualize_images(path, target_size=IMAGE_SIZE, num_images=5):
    """Show random sample images from a class directory."""
    image_filenames = [f for f in path.iterdir() if f.is_file()]
    if not image_filenames:
        raise ValueError(f"No images found in: {path}")

    selected = random.sample(image_filenames, min(num_images, len(image_filenames)))
    fig, axes = plt.subplots(1, len(selected), figsize=(15, 3), facecolor="white")
    if len(selected) == 1:
        axes = [axes]

    for axis, image_path in zip(axes, selected):
        img = Image.open(image_path).resize(target_size)
        axis.imshow(img)
        axis.axis("off")
        axis.set_title(image_path.name)

    plt.tight_layout()
    plt.show()


def build_datasets(dataset_dir):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        batch_size=BATCH_SIZE,
        image_size=IMAGE_SIZE,
        seed=SEED,
        shuffle=True,
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        batch_size=BATCH_SIZE,
        image_size=IMAGE_SIZE,
        seed=SEED,
        shuffle=False,
    )

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=autotune)
    val_ds = val_ds.cache().prefetch(buffer_size=autotune)
    return train_ds, val_ds


def build_model(num_classes):
    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
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
    return model


def plot_training_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(history.history["accuracy"], label="Train", marker="o")
    ax1.plot(history.history["val_accuracy"], label="Validation", marker="o")
    ax1.set(xlabel="Epoch", ylabel="Accuracy", title="Accuracy")
    ax1.legend()

    ax2.plot(history.history["loss"], label="Train", marker="o")
    ax2.plot(history.history["val_loss"], label="Validation", marker="o")
    ax2.set(xlabel="Epoch", ylabel="Loss", title="Loss")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(TRAINING_PLOT_PATH, dpi=150)
    plt.show()


def main():
    if not DATASET_DIR.exists():
        raise FileNotFoundError(f"Dataset directory not found: {DATASET_DIR}")

    class_names = get_class_names(DATASET_DIR)
    if not class_names:
        raise ValueError(f"No class folders found in: {DATASET_DIR}")

    print("Class Names:", class_names)
    print("Num Classes:", len(class_names))

    for class_name in class_names:
        class_dir = DATASET_DIR / class_name
        print(f"\nSample images - {class_name}")
        visualize_images(class_dir, num_images=5)

    train_ds, val_ds = build_datasets(DATASET_DIR)
    model = build_model(len(class_names))
    model.summary()

    early_stopping = callbacks.EarlyStopping(
        patience=3,
        restore_best_weights=True,
        monitor="val_accuracy",
    )

    history = model.fit(
        train_ds,
        epochs=25,
        validation_data=val_ds,
        callbacks=[early_stopping],
    )

    model.save(MODEL_SAVE_PATH)
    print(f"\nModel saved -> {MODEL_SAVE_PATH}")

    model.export(str(SAVED_MODEL_DIR))
    print(f"SavedModel exported -> {SAVED_MODEL_DIR}")

    np.save(CLASS_NAMES_PATH, np.array(class_names))
    print(f"Class names saved -> {CLASS_NAMES_PATH}")

    plot_training_history(history)
    print(f"Training plot saved -> {TRAINING_PLOT_PATH}")


if __name__ == "__main__":
    main()
