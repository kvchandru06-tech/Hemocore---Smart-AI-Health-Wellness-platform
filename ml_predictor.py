# ml_predictor.py
import joblib
import numpy as np
import os

class BloodRiskPredictor:
    def __init__(self, model_path="blood_risk_model.pkl"):
        """Load the trained ML model"""
        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                self.model_loaded = True
                print("✅ ML Model loaded successfully")
            else:
                self.model = None
                self.model_loaded = False
                print(f"⚠️ ML Model file not found at: {os.path.abspath(model_path)}")
        except Exception as e:
            self.model = None
            self.model_loaded = False
            print(f"❌ Error loading model: {e}")
    
    def predict_risk(self, features: dict) -> dict:
        """Predict health risk from blood features"""
        if not self.model_loaded:
            return {
                "risk_level": "Unknown (Model not loaded)",
                "confidence": 0.0,
                "is_high_risk": False,
                "message": "ML model not available"
            }
        
        # Your model was trained on these 6 features in EXACT order:
        # [Hemoglobin, Fasting_Blood_Sugar, LDL, HDL, Triglycerides, Vitamin_D]
        
        # Get values from features dictionary (use defaults if missing)
        X = np.array([[
            features.get('Hemoglobin', 13.5),      # Feature 1
            features.get('Fasting_Blood_Sugar', 90), # Feature 2
            features.get('LDL', 100),              # Feature 3
            features.get('HDL', 50),               # Feature 4
            features.get('Triglycerides', 150),    # Feature 5
            features.get('Vitamin_D', 30)          # Feature 6
        ]])
        
        try:
            # Make prediction
            prediction = self.model.predict(X)[0]  # 0 or 1
            probabilities = self.model.predict_proba(X)[0]  # [prob_normal, prob_high_risk]
            
            # Interpret results
            is_high_risk = (prediction == 1)
            confidence = probabilities[1] if is_high_risk else probabilities[0]
            
            return {
                "risk_level": "HIGH RISK" if is_high_risk else "NORMAL",
                "confidence": float(confidence * 100),  # as percentage
                "is_high_risk": bool(is_high_risk),
                "prediction_code": int(prediction),
                "probabilities": {
                    "normal": float(probabilities[0] * 100),
                    "high_risk": float(probabilities[1] * 100)
                },
                "message": "Consider consulting a doctor" if is_high_risk else "Results appear normal"
            }
        except Exception as e:
            return {
                "risk_level": "Error in prediction",
                "confidence": 0.0,
                "is_high_risk": False,
                "message": f"Prediction error: {str(e)}"
            }

# Create a global instance
predictor = BloodRiskPredictor()