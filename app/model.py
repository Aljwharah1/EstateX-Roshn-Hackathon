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
        """Return predicted price or None if model doesn't exist or features insufficient"""
        if self.model is None:
            return None

        # Model expects 15 features: 6 base + 1 district_encoded + 8 location one-hots
        # Currently we only have 8 features in self.feature_names, so we cannot properly
        # reconstruct the full feature vector. Return None for now.
        # TODO: Retrain model with proper feature list and save district encoder + location OHE to encoders.pkl
        return None
