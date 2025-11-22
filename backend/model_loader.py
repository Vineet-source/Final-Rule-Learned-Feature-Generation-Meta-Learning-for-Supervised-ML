import xgboost as xgb
import os
from config import MODEL_PATH  

def load_model():
    if not os.path.exists(MODEL_PATH):
        print(f"⚠️ WARNING: Model file '{MODEL_PATH}' not found. App will run but predictions will fail.")
        return xgb.XGBClassifier()
        
    try:
        model = xgb.XGBClassifier()
        model.load_model(MODEL_PATH)
        print(f"✅ Model loaded from {MODEL_PATH}")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return xgb.XGBClassifier()

model = load_model()