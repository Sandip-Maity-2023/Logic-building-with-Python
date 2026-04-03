from model import predict
from gemini import generate_response

def run_workflow(image):

    prediction = predict(image)

    disease = prediction[0]['label']
    confidence = prediction[0]['score']

    explanation = generate_response(disease)

    return {
        "disease": disease,
        "confidence": confidence,
        "explanation": explanation
    }