import os
import pickle
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "model.pkl")

# Load model once when service starts
model_data = None

def load_model():
    global model_data
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    print("ML model loaded successfully")

def predict_failure(amount, payment_method, gateway, hour):
    if model_data is None:
        load_model()
    
    le_method = model_data['le_method']
    le_gateway = model_data['le_gateway']
    model = model_data['model']

    try:
        method_enc = le_method.transform([payment_method])[0]
    except:
        method_enc = 0

    try:
        gateway_enc = le_gateway.transform([gateway])[0]
    except:
        gateway_enc = 0

    is_peak_hour = 1 if 20 <= hour <= 21 else 0
    is_high_amount = 1 if amount > 3000 else 0

    features = np.array([[
        amount,
        method_enc,
        gateway_enc,
        hour,
        is_peak_hour,
        is_high_amount
    ]])

    prob = model.predict_proba(features)[0][1]
    prediction = int(prob > 0.5)

    return {
        "failure_probability": round(float(prob), 4),
        "predicted_failure": bool(prediction),
        "risk_level": "HIGH" if prob > 0.6 else "MEDIUM" if prob > 0.3 else "LOW"
    }