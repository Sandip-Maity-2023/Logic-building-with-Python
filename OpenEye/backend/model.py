from transformers import pipeline

classifier = pipeline(
    "image-classification",
    model="dima806/retinal-disease-classifier"
)

def predict(image):
    result = classifier(image)
    return result