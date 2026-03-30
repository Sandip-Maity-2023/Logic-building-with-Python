import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np

SHOW_TRAINING_IMAGES = False
SHOW_SINGLE_PREDICTION = True
SHOW_MULTIPLE_PREDICTIONS = False

# Load CIFAR10 dataset
print("Loading CIFAR-10 dataset...")
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
print("Dataset loaded successfully.")

# normalize
train_images, test_images = train_images / 255.0, test_images / 255.0

# class names
class_names = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

# Show training images
if SHOW_TRAINING_IMAGES:
    plt.figure(figsize=(10, 10))

    for i in range(9):
        plt.subplot(3, 3, i + 1)
        plt.imshow(train_images[i])
        plt.title(class_names[train_labels[i][0]])
        plt.axis('off')

    plt.tight_layout()
    plt.show()

# Build CNN Model
model = models.Sequential([
    layers.Input(shape=(32, 32, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10),
])

# Compile
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])
model.summary()

# Train
print("Starting training...")
history = model.fit(
    train_images,
    train_labels,
    epochs=10,
    validation_data=(test_images, test_labels))
print("Training completed.")

# Evaluate
print("Evaluating model...")
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("Test Accuracy:", test_acc)

# Predict
print("Running predictions...")
prediction_count = 9 if SHOW_MULTIPLE_PREDICTIONS else 1
predictions = model.predict(test_images[:prediction_count])

# Show one test image
index = 0
predicted_label = np.argmax(predictions[index])

print("Predicted Class:", class_names[predicted_label])
print("Actual Class:", class_names[test_labels[index][0]])

if SHOW_SINGLE_PREDICTION:
    plt.imshow(test_images[index])
    plt.title(
        "Predicted: " + class_names[predicted_label]
        + " | Actual: " + class_names[test_labels[index][0]])
    plt.axis('off')
    plt.show()

# Show multiple test images
if SHOW_MULTIPLE_PREDICTIONS:
    plt.figure(figsize=(10, 10))

    for i in range(9):
        plt.subplot(3, 3, i + 1)
        plt.imshow(test_images[i])
        plt.title(
            "P: " + class_names[np.argmax(predictions[i])]
            + "\nA: " + class_names[test_labels[i][0]])
        plt.axis('off')

    plt.tight_layout()
    plt.show()
