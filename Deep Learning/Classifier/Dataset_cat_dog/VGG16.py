from pathlib import Path

from tensorflow.keras import layers, mixed_precision, models
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator

mixed_precision.set_global_policy("mixed_float16")

BASE_DIR = Path(__file__).resolve().parent
TRAIN_PATH = BASE_DIR / "train"
VAL_PATH = BASE_DIR / "test"

# =========================
# Parameters
# =========================
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 10

if not TRAIN_PATH.exists():
    raise FileNotFoundError(f"Training folder not found: {TRAIN_PATH}")

if not VAL_PATH.exists():
    raise FileNotFoundError(f"Validation folder not found: {VAL_PATH}")

# =========================
# Data Generators
# =========================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    shear_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    str(TRAIN_PATH),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

val_data = val_datagen.flow_from_directory(
    str(VAL_PATH),
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# =========================
# Load VGG16 Model
# =========================
base_model = VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze convolution layers
for layer in base_model.layers:
    layer.trainable = False

# =========================
# Custom Classifier (FAST)
# =========================
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)
output = layers.Dense(1, activation="sigmoid", dtype="float32")(x)

model = models.Model(inputs=base_model.input, outputs=output)

# =========================
# Compile
# =========================
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================
# Train
# =========================
history = model.fit(
    train_data,
    epochs=EPOCHS,
    validation_data=val_data
)
# =========================
# Save Model
# =========================
model.save(str(BASE_DIR / "vgg16_cat_dog.h5"))

print("Model Saved Successfully")
