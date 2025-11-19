# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from .recommender import RuleBasedRecommender
from .model import ForecastModel

from typing import List, Optional

app = FastAPI(title="Real Estate Recommender API")

# ---- Load dataset ----
DATA_PATH = "data/Finalized_Data.xlsx"
df = pd.read_excel(DATA_PATH)

# ---- Initialize engines ----
recommender = RuleBasedRecommender(df)
forecast_model = ForecastModel()

# Wrap recommender.recommend with a simple fallback: if no results, return top-20 overall
_orig_recommend = recommender.recommend

def _recommend_with_fallback(prefs: dict):
    try:
        res = _orig_recommend(prefs)
        # If we got results, return them
        if isinstance(res, pd.DataFrame) and res.shape[0] > 0:
            return res.head(20)
    except Exception:
        pass

    # Fallback: return top 20 items by score (no filters)
    # Recompute score for all items
    fallback = recommender.df.copy()
    g = prefs.get("goal", "")
    if g == "investment":
        fallback["score"] = -fallback["price_per_sqm"].fillna(0)
    elif g == "residential":
        fallback["score"] = fallback["area_sqm"].fillna(0)
    else:
        fallback["score"] = 0

    return fallback.sort_values(by="score", ascending=False).reset_index(drop=True).head(20)

recommender.recommend = _recommend_with_fallback


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
    try:
        results = recommender.recommend(prefs.dict())
    except Exception as e:
        # If recommend fails, return empty
        results = pd.DataFrame()
    
    # If empty after recommend, return top 20 by price_per_sqm
    if len(results) == 0:
        results = recommender.df.copy()
        results = results.dropna(subset=["price_per_sqm"]).sort_values(by="price_per_sqm").head(20)
    else:
        results = results.head(20)

    if len(results) == 0:
        return []

    # Add forecast price for each property (may be None if model features don't match)
    results["forecast_price"] = results.apply(
        lambda r: forecast_model.predict_price(r), axis=1
    )
    
    # Convert to dict, removing rows with None forecast_price for now
    output = results.to_dict(orient="records")
    return output


@app.get("/")
def root():
    # serve the frontend index
    return FileResponse("frontend/index.html")


@app.post("/ask")
def ask_ai(payload: dict):
    user_message = payload.get("message", "")
    # Import here to avoid import-time issues and circular imports
    from .llm import ask_llm
    answer = ask_llm(user_message)
    return {"answer": answer}

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Note: StaticFiles mounted at root will serve `index.html` and other frontend assets.
