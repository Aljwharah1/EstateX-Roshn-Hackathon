# app/chatbot.py

import os
from openai import OpenAI
from app.model import ForecastModel
from app.recommender import RuleBasedRecommender
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load dataset and create instances for use by the LLM functions
DATA_PATH = "data/Finalized_Data.xlsx"
_df = pd.read_excel(DATA_PATH)
_recommender = RuleBasedRecommender(_df)
_forecaster = ForecastModel("models/xgb_model.json", "models/encoders.pkl")

SYSTEM_PROMPT = """
You are EstateX Advisor’s AI assistant.

You DO NOT use outside internet or any external knowledge.

You ONLY use:
1) The XGBoost model for price predictions
2) The rule-based recommender system
3) The structured dataset summaries provided internally

If the user asks for anything outside these sources, respond:
"Sorry, I can only answer based on the project’s internal models and dataset."

When appropriate, call one of the provided functions.
"""

def call_llm(user_message: str):

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        functions=[
            {
                "name": "predict_price",
                "description": "Predict price per sqm using the XGBoost model.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "region": {"type": "string"},
                        "city": {"type": "string"},
                        "property_class": {"type": "string"},
                        "property_type": {"type": "string"},
                        "district": {"type": "string"},
                        "location": {"type": "string"},
                        "area_sqm": {"type": "number"},
                        "year": {"type": "number"}
                    },
                    "required": ["district", "location", "area_sqm", "year"]
                }
            },
            {
                "name": "recommend_properties",
                "description": "Return filtered properties based on user preferences.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "min_budget": {"type": "number"},
                        "max_budget": {"type": "number"},
                        "district": {"type": "string"},
                        "property_class": {"type": "string"},
                        "goal": {"type": "string"}
                    }
                }
            }
        ]
    )

    # If LLM wants to call a function:
    if response.choices[0].finish_reason == "function_call":
        fn = response.choices[0].message.function_call
        name = fn.name
        args = eval(fn.arguments)

        if name == "predict_price":
            # args is a dict of the feature values
            series = pd.Series(args)
            pred = _forecaster.predict_price(series)
            result = {"price_per_sqm": pred}
        elif name == "recommend_properties":
            # args may contain filtering prefs
            prefs = args if isinstance(args, dict) else {}
            recs = _recommender.recommend(prefs)
            result = recs.to_dict(orient="records")
        else:
            result = {"error": "Unknown function"}

        return result

    # Otherwise return normal LLM text
    return response.choices[0].message["content"]
