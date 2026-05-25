from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np
import pickle

app = Flask(__name__)

CORS(app)

# =========================
# LOAD MODEL & SCALER
# =========================

model = pickle.load(open('trained_model2.sav', 'rb'))

scaler = pickle.load(open('scaler.sav', 'rb'))

# =========================
# PREDICTION FUNCTION
# =========================

def diabetes_prediction(input_data):

    input_data_as_numpy_array = np.asarray(input_data)

    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    # scale input
    scaled_data = scaler.transform(input_data_reshaped)

    prediction = model.predict(scaled_data)

    probability = model.predict_proba(scaled_data)

    confidence = float(np.max(probability) * 100)

    if prediction[0] == 0:
        result = 'The person is NOT diabetic'
    else:
        result = 'The person IS diabetic'

    return result, confidence

# =========================
# API ROUTE
# =========================

@app.route('/predict', methods=['POST'])

def predict():

    data = request.json

    input_data = [

        float(data['Pregnancies']),
        float(data['Glucose']),
        float(data['BloodPressure']),
        float(data['SkinThickness']),
        float(data['Insulin']),
        float(data['BMI']),
        float(data['DiabetesPedigreeFunction']),
        float(data['Age'])
    ]

    result, confidence = diabetes_prediction(input_data)

    return jsonify({

        'prediction': result,
        'confidence': round(confidence, 2)

    })

# =========================
# MAIN
# =========================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)