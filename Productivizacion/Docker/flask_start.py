from flask import Flask
import joblib

# Flask start
app = Flask(__name__)

# Load model and encoders
label_encoder = joblib.load('model/label_encoders1.pkl')
model = joblib.load('model/model_xgb_optimized.pkl')

def get_label_encoder():
    return label_encoder

def get_model():
    return model
