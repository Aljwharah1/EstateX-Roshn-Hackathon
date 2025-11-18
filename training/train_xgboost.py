# training/train_xgboost.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import xgboost as xgb
from pathlib import Path
import pickle

DATA_PATH = "data/Finalized_Data.xlsx"
MODEL_PATH = "models/xgb_model.json"

print("📌 Loading dataset...")
df = pd.read_excel(DATA_PATH)

# -----------------------------
# 1. Clean dataset
# -----------------------------
print("📌 Cleaning dataset...")

# Convert numerical
df["price_sar"] = pd.to_numeric(df["price_sar"], errors="coerce")
df["area_sqm"] = pd.to_numeric(df["area_sqm"], errors="coerce")
df["price_per_sqm"] = pd.to_numeric(df["price_per_sqm"], errors="coerce")

# Drop rows without a target
df = df.dropna(subset=["price_per_sqm"])

# Fill missing area with median
df["area_sqm"].fillna(df["area_sqm"].median(), inplace=True)

# Fill missing property_type with "unknown"
df["property_type"].fillna("غير معروف", inplace=True)

# Fill missing location with mode
df["location"].fillna(df["location"].mode()[0], inplace=True)

# -----------------------------
# 2. Encode Arabic categorical columns
# -----------------------------

categorical_cols = ["region", "city", "property_class", "property_type", "district", "location", "quarter"]

encoders = {}
for col in categorical_cols:
    enc = LabelEncoder()
    df[col] = df[col].astype(str)
    df[col] = enc.fit_transform(df[col])
    encoders[col] = enc

print("📌 Encoded categorical variables.")

# -----------------------------
# 3. Select features + target
# -----------------------------

TARGET = "price_per_sqm"

FEATURES = [
    "region", "city",
    "property_class", "property_type",
    "district", "location",
    "area_sqm", "year"
]

X = df[FEATURES]
y = df[TARGET]

# -----------------------------
# 4. Train/Test Split
# -----------------------------

print("📌 Splitting into train and test...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 5. Train XGBoost
# -----------------------------

print("📌 Training XGBoost model...")

model = xgb.XGBRegressor(
    n_estimators=400,
    learning_rate=0.08,
    max_depth=7,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# 6. Evaluate
# -----------------------------

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

print(f"✅ Model trained successfully. MAE = {mae:,.2f} SAR per sqm")

# -----------------------------
# 7. Save model and encoders
# -----------------------------

Path("models").mkdir(exist_ok=True)
model.save_model(MODEL_PATH)

# Save encoders for later use
with open("models/encoders.pkl", 'wb') as f:
    pickle.dump(encoders, f)

print(f"🎉 Model saved to: {MODEL_PATH}")
print(f"🎉 Encoders saved to: models/encoders.pkl")