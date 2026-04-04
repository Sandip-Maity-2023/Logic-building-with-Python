from model import predict
from gemini import generate_response

def run_workflow(image):

    prediction = predict(image)
    if not prediction:
        raise RuntimeError("The model did not return any prediction.")

    disease = prediction[0]['label']
    confidence = prediction[0]['score']

    explanation = generate_response(disease)

    return {
        "disease": disease,
        "confidence": confidence,
        "explanation": explanation
    }
