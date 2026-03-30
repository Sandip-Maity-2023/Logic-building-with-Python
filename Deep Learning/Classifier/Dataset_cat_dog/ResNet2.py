from pathlib import Path

import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ======================
# Parameters
# ======================
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 10

BASE_DIR = Path.cwd()
if not (BASE_DIR / "Classifier").exists():
    BASE_DIR = BASE_DIR / "Deep Learning"
train_path = BASE_DIR / "Classifier" / "Dataset_cat_dog" / "train"
val_path = BASE_DIR / "Classifier" / "Dataset_cat_dog" / "test"
model_path = BASE_DIR / "resnet50_cat_dog.h5"

if not train_path.exists():
    raise FileNotFoundError(f"Training folder not found: {train_path}")

if not val_path.exists():
    raise FileNotFoundError(f"Validation folder not found: {val_path}")

# ======================
# Data Generators
# ======================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    str(train_path),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

val_data = val_datagen.flow_from_directory(
    str(val_path),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# ======================
# Load ResNet50
# ======================
base_model = ResNet50(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

# Freeze base model
for layer in base_model.layers:
    layer.trainable = False

# ======================
# Custom Head
# ======================
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)
output = layers.Dense(1, activation='sigmoid', dtype='float32')(x)

model = models.Model(inputs=base_model.input, outputs=output)

# ======================
# Compile
# ======================
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ======================
# Train
# ======================
history = model.fit(
    train_data,
    epochs=EPOCHS,
    validation_data=val_data
)
print("Training Accuracy:", history.history['accuracy'][-1])
print("Validation Accuracy:", history.history['val_accuracy'][-1])
# ======================
# Save Model
# ======================
model.save(str(model_path))

print("Training Finished")