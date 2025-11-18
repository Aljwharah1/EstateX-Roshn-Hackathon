# app/model.py
import xgboost as xgb
import pandas as pd
import numpy as np
from pathlib import Path
import pickle

class ForecastModel:
    def __init__(self, model_path: str = "models/xgb_model.json", encoder_path: str = "models/encoders.pkl"):
        self.model_path = Path(model_path)
        self.encoder_path = Path(encoder_path)
        self.model = None
        self.encoders = {}
        self.feature_names = [
            "region", "city",
            "property_class", "property_type",
            "district", "location",
            "area_sqm", "year"
        ]
        
        if self.model_path.exists() and self.encoder_path.exists():
            self.model = xgb.XGBRegressor()
            self.model.load_model(str(model_path))
            with open(encoder_path, 'rb') as f:
                self.encoders = pickle.load(f)
        else:
            print("⚠️ No XGBoost model found — forecasting will return None.")

    def predict_price(self, row: pd.Series):
        """Return predicted price or None if model doesn't exist"""
        if self.model is None:
            return None

        # Extract only the required features
        features = []
        for feat in self.feature_names:
            if feat in row.index:
                val = row[feat]
                # Encode categorical features
                if feat in self.encoders:
                    if pd.isna(val):
                        val = 0
                    else:
                        try:
                            val = self.encoders[feat].transform([str(val)])[0]
                        except:
                            val = 0
                features.append(val if not pd.isna(val) else 0)
            else:
                features.append(0)
        
        features = np.array(features).reshape(1, -1)
        return float(self.model.predict(features)[0])
