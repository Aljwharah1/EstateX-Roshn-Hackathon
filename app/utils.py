# app/utils.py
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib

def load_data(path="data/Finalized_Data.xlsx"):
    df = pd.read_excel(path)
    # minimal cleaning
    df['price_sar'] = pd.to_numeric(df['price_sar'], errors='coerce')
    df['area_sqm'] = pd.to_numeric(df['area_sqm'], errors='coerce')
    df.dropna(subset=['price_sar', 'area_sqm'], inplace=True)
    return df

def build_preprocessor(df):
    # Example: encode district and property_type; scale numeric
    cat_cols = ['district','property_type']
    num_cols = ['area_sqm','price_per_sqm']
    ohe = OneHotEncoder(handle_unknown='ignore')
    scaler = StandardScaler()
    # Fit on df
    ohe.fit(df[cat_cols].astype(str))
    scaler.fit(df[num_cols])
    joblib.dump({'ohe': ohe, 'scaler': scaler}, "models/preprocessing.joblib")
    return {'ohe': ohe, 'scaler': scaler}