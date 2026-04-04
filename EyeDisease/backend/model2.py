import os
import cv2
import random
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')


BASE_DIR = Path(__file__).resolve().parent
MODEL_SAVE_PATH = BASE_DIR / "eye_disease_mobilenet.h5"
CLASS_NAMES_PATH = BASE_DIR / "class_names.npy"

# FIX 1: use stable path relative to this file
train_dir = BASE_DIR / "dataset"


# Load training dataset
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.2,
    subset='training',
    batch_size=24,
    image_size=(256, 256),
    seed=123,
    shuffle=True,
)

# Load validation dataset
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.2,
    subset='validation',
    batch_size=32,
    image_size=(256, 256),
    seed=123,
)

# FIX 2: correct class names
class_names = train_ds.class_names
num_classes = len(class_names)

print("Class Names:", class_names)
print("Number of Classes:", num_classes)


def visualize_images(path, target_size=(256, 256), num_images=5):
    image_filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    selected_images = random.sample(image_filenames, min(num_images, len(image_filenames)))

    fig, axes = plt.subplots(1, num_images, figsize=(15, 3))

    for i, image_filename in enumerate(selected_images):
        image_path = os.path.join(path, image_filename)
        image = Image.open(image_path)
        image = image.resize(target_size)

        axes[i].imshow(image)
        axes[i].axis('off')
        axes[i].set_title(image_filename)

    plt.tight_layout()
    plt.show()


# visualize samples
visualize_images(r"EyeDisease/backend/dataset/cataract")
visualize_images(r"EyeDisease/backend/dataset/glaucoma")
visualize_images(r"EyeDisease/backend/dataset/diabetic_retinopathy")
visualize_images(r"EyeDisease/backend/dataset/normal")


# performance optimization
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


# augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip('horizontal'),
    layers.RandomRotation(0.2),
])


# MobileNetV2
base_model = tf.keras.applications.MobileNetV2(
    include_top=False,
    weights='imagenet',
    input_shape=(256, 256, 3)
)

base_model.trainable = False


# Model
inputs = tf.keras.Input(shape=(256,256,3))
x = data_augmentation(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)

# FIX: add softmax for inference-friendly output
outputs = layers.Dense(num_classes, activation='softmax')(x)

model = tf.keras.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()


# Early stopping
early_stopping = callbacks.EarlyStopping(
    patience=3,
    restore_best_weights=True
)


# Train
history = model.fit(
    train_ds,
    epochs=25,
    validation_data=val_ds,
    callbacks=[early_stopping]
)


# Accuracy plot
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.show()


# Loss plot
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.show()


# =========================
# SAVE MODEL (IMPORTANT)
# =========================

model.save(MODEL_SAVE_PATH)
np.save(CLASS_NAMES_PATH, np.array(class_names))

print(f"Model saved successfully! -> {MODEL_SAVE_PATH}")
print(f"Class names saved successfully! -> {CLASS_NAMES_PATH}")
