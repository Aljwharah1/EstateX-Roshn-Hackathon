from fastapi import FastAPI
from models.schemas import UserPreferences, RecommendationResponse
from recommender import RuleBasedRecommender

app = FastAPI(
    title="EstateX Advisor API",
    description="AI-powered real estate rule-based recommender system",
    version="1.0.0"
)

# Load recommender on app startup
recommender = RuleBasedRecommender("data/Real Estate Data.xlsx")


@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(prefs: UserPreferences):
    results = recommender.recommend(prefs.dict())

    # Convert DataFrame to dict list
    recommendations = results.to_dict(orient="records")

    return {"results": recommendations}
