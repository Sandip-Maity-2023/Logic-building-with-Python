import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np

# ===============================
# Load CIFAR10 dataset (fixed spelling)

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# normalize
train_images, test_images = train_images/255.0, test_images/255.0

# class names
class_names = ['airplane','automobile','bird','cat','deer',
               'dog','frog','horse','ship','truck']

# Show sample images
plt.figure(figsize=(10,10))

for i in range(9):
    plt.subplot(3,3,i+1)
    plt.imshow(train_images[i])
    plt.title(class_names[train_labels[i][0]])
    plt.axis('off')

plt.show()

# Create CNN Model (fixed)
model = models.Sequential()

model.add(layers.Conv2D(
    32,
    (3,3),
    activation='relu',
    input_shape=(32,32,3)
))

model.add(layers.MaxPooling2D((2,2)))

model.add(layers.Conv2D(
    64,
    (3,3),
    activation='relu'
))

model.add(layers.MaxPooling2D((2,2)))

model.add(layers.Conv2D(
    64,
    (3,3),
    activation='relu'
))

# Flatten
model.add(layers.Flatten())

# Dense layer
model.add(layers.Dense(64, activation='relu'))

# Output layer (10 classes)
model.add(layers.Dense(10))

# Compile
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

model.summary()

# Train
history = model.fit(
    train_images,
    train_labels,
    epochs=10,
    validation_data=(test_images, test_labels)
)

# Evaluate
test_loss, test_acc = model.evaluate(test_images, test_labels)

print("Test Accuracy:", test_acc)

# Prediction
predictions = model.predict(test_images)

predicted_label = np.argmax(predictions[0])

print("Predicted Class:", class_names[predicted_label])
print("Actual Class:", class_names[test_labels[0][0]])

# show image
plt.imshow(test_images[0])
plt.title("Predicted: " + class_names[predicted_label])
plt.axis('off')
plt.show()