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
    prefs_dict = prefs.dict()
    print(f"===ENDPOINT CALLED===")
    print(f"  location: {prefs_dict.get('location')} (type: {type(prefs_dict.get('location'))})")
    print(f"  property_type: {prefs_dict.get('property_type')}")
    print(f"  min_budget: {prefs_dict.get('min_budget')}")
    print(f"  max_budget: {prefs_dict.get('max_budget')}")
    
    try:
        results = recommender.recommend(prefs_dict)
        print(f"===RECOMMENDER RETURNED=== {len(results)} results")
    except Exception as e:
        print(f"Error in recommender: {e}")
        results = pd.DataFrame()
    
    # Limit to top 20 - no fallback logic
    if len(results) > 0:
        results = results.head(20)

    if len(results) == 0:
        return []

    # Add forecast price for each property (may be None if model features don't match)
    results["forecast_price"] = results.apply(
        lambda r: forecast_model.predict_price(r), axis=1
    )
    
    # If goal is long-term investment, add future revenue forecasts
    goal = prefs_dict.get("goal", "")
    if goal == "investment":
        # Assume annual appreciation rate (e.g., 5%)
        appreciation_rate = 0.05
        def forecast_revenue(row, years):
            price = row["price_sar"]
            if pd.isnull(price):
                return None
            return round(price * ((1 + appreciation_rate) ** years), 2)
        results["revenue_5y"] = results.apply(lambda r: forecast_revenue(r, 5), axis=1)
        results["revenue_10y"] = results.apply(lambda r: forecast_revenue(r, 10), axis=1)
        results["revenue_20y"] = results.apply(lambda r: forecast_revenue(r, 20), axis=1)
    
    # Convert to dict
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
