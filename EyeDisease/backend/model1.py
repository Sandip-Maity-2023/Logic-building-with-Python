import os
import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
from tensorflow.keras import callbacks

import warnings
warnings.filterwarnings('ignore')


# ─── Paths ────────────────────────────────────────────────────────────────────
train_dir = 'EyeDisease/backend/dataset'   # use forward slashes (works on all OS)
MODEL_SAVE_PATH = 'eye_disease_model.keras'  # saved model path


# ─── Load Datasets ────────────────────────────────────────────────────────────
# BUG FIX: both splits must share the same seed so the 80/20 split is consistent

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.2,
    subset='training',
    batch_size=24,
    image_size=(256, 256),
    seed=42,          # ← fixed (was 123, mismatched with val_ds)
    shuffle=True,
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    validation_split=0.2,
    subset='validation',
    batch_size=32,
    image_size=(256, 256),
    seed=42,
    shuffle=False,    # no need to shuffle validation data
)


# ─── Class Info ───────────────────────────────────────────────────────────────
class_names = sorted(os.listdir(train_dir))
num_classes  = len(class_names)
print("Class Names :", class_names)
print("Num Classes :", num_classes)


# ─── Image Visualizer ─────────────────────────────────────────────────────────
# BUG FIX: the original code had the visualize calls INSIDE the function body
# due to a missing blank line / wrong indentation level — moved them outside.

def visualize_images(path, target_size=(256, 256), num_images=5):
    """Show num_images random samples from a directory."""
    image_filenames = [
        f for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]
    if not image_filenames:
        raise ValueError("No images found in the specified path")

    selected = random.sample(image_filenames, min(num_images, len(image_filenames)))

    fig, axes = plt.subplots(1, num_images, figsize=(15, 3), facecolor='white')
    for i, fname in enumerate(selected):
        img = Image.open(os.path.join(path, fname)).resize(target_size)
        axes[i].imshow(img)
        axes[i].axis('off')
        axes[i].set_title(fname)
    plt.tight_layout()
    plt.show()


# Visualise samples from each class  ← these were INSIDE the function before!
for class_name in class_names:
    print(f"\nSample images — {class_name}")
    visualize_images(os.path.join(train_dir, class_name), num_images=5)


# ─── Performance Optimisation ─────────────────────────────────────────────────
AUTOTUNE = tf.data.experimental.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds   = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


# ─── Data Augmentation ────────────────────────────────────────────────────────
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.5),
])


# ─── Transfer Learning — MobileNetV2 ──────────────────────────────────────────
base_model = tf.keras.applications.MobileNetV2(
    include_top=False,
    weights='imagenet',
    input_shape=(256, 256, 3),
)
base_model.trainable = False          # freeze the base during initial training

preprocess_input      = tf.keras.applications.mobilenet_v2.preprocess_input
global_average_layer  = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer      = tf.keras.layers.Dense(num_classes)

# BUG FIX: removed the unused `rescale` layer that was defined but never added
# to the model graph (it was a dead variable causing silent confusion).

inputs  = tf.keras.Input(shape=(256, 256, 3))
x       = data_augmentation(inputs)
x       = preprocess_input(x)
x       = base_model(x, training=False)
x       = global_average_layer(x)
x       = tf.keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)

model = tf.keras.Model(inputs=inputs, outputs=outputs)


# ─── Compile ──────────────────────────────────────────────────────────────────
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'],
)

model.summary()


# ─── Train ────────────────────────────────────────────────────────────────────
early_stopping = callbacks.EarlyStopping(
    patience=3,
    restore_best_weights=True,   # restore the best epoch's weights on stop
    monitor='val_accuracy',
)

history = model.fit(
    train_ds,
    epochs=25,
    validation_data=val_ds,
    callbacks=[early_stopping],
)


# ─── Save the Model ───────────────────────────────────────────────────────────
# Primary format: native Keras v3 (.keras) — recommended
model.save(MODEL_SAVE_PATH)
print(f"\n✅ Model saved  →  {MODEL_SAVE_PATH}")

# Also export as TensorFlow SavedModel folder (for TF-Serving / TFLite etc.)
model.export('eye_disease_savedmodel')
print("✅ SavedModel exported  →  eye_disease_savedmodel/")

# Save class names alongside the model so prediction works without the dataset
np.save('class_names.npy', np.array(class_names))
print("✅ Class names saved  →  class_names.npy")


# ─── Plots ────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(history.history['accuracy'],     label='Train',      marker='o')
ax1.plot(history.history['val_accuracy'], label='Validation', marker='o')
ax1.set(xlabel='Epoch', ylabel='Accuracy', title='Accuracy')
ax1.legend()

ax2.plot(history.history['loss'],     label='Train',      marker='o')
ax2.plot(history.history['val_loss'], label='Validation', marker='o')
ax2.set(xlabel='Epoch', ylabel='Loss', title='Loss')
ax2.legend()

plt.tight_layout()
plt.savefig('training_history.png', dpi=150)
plt.show()
print("✅ Training plot saved  →  training_history.png")


