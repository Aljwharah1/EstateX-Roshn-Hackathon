# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from app.recommender import RuleBasedRecommender
from app.model import ForecastModel

from typing import List, Optional
from app.chatbot import generate_reply
from .llm import ask_llm

app = FastAPI(title="Real Estate Recommender API")

# ---- Load dataset ----
DATA_PATH = "data/Finalized_Data.xlsx"
df = pd.read_excel(DATA_PATH)

# ---- Initialize engines ----
recommender = RuleBasedRecommender(df)
forecast_model = ForecastModel()


class UserPrefs(BaseModel):
    min_budget: float | None = None
    max_budget: float | None = None
    property_type: list[str] | None = None
    property_class: list[str] | None = None
    district: list[str] | None = None
    location: list[str] | None = None
    goal: str | None = None


@app.post("/recommend")
def recommend_properties(prefs: UserPrefs):
    results = recommender.recommend(prefs.dict())
    
    if len(results) == 0:
        return []

    # Add forecast (optional)
    results["forecast_price"] = results.apply(
        lambda r: forecast_model.predict_price(r), axis=1
    )

    return results.head(20).to_dict(orient="records")


@app.get("/")
def root():
    return {"message": "Real Estate API running"}


@app.post("/ask")
def ask_endpoint(payload: dict):
    user_message = payload["message"]
    answer = ask_llm(user_message)
    return {"answer": answer}