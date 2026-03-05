# app/chatbot.py

import os
from openai import OpenAI
from app.recommender import RuleBasedRecommender
from models.model import ForecastModel
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize recommender (no data needed at init time - data comes from Supabase)
_recommender = RuleBasedRecommender()
_forecaster = ForecastModel("models/xgb_model.json", "models/encoders.pkl")

SYSTEM_PROMPT = """
You are EstateX Advisor’s AI assistant.

You DO NOT use outside internet or any external knowledge.

You ONLY use:
1) The XGBoost model for price predictions
2) The rule-based recommender system
3) The Supabase database with properties, transactions, and user data

If the user asks for anything outside these sources, respond:
"Sorry, I can only answer based on the project's internal models and Supabase database."

When appropriate, call one of the provided functions.
"""

def call_llm(user_message: str, sb=None):
    """
    Call LLM with function callbacks for recommendations and price predictions.
    
    Args:
        user_message: User's message
        sb: Supabase client for data queries (optional - for advanced usage)
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
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
                "description": "Return filtered properties based on user preferences from Supabase.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "min_budget": {"type": "number"},
                        "max_budget": {"type": "number"},
                        "district": {"type": "string"},
                        "property_type": {"type": "string"},
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
            # Call the forecaster with the provided features
            pred = _forecaster.predict_price_from_dict(args)
            result = {"price_per_sqm": pred}
        elif name == "recommend_properties":
            # Note: This would require fetching data from Supabase first
            # For now, return a message requesting Supabase client
            if sb is None:
                result = {"message": "Supabase client required for recommendations"}
            else:
                # TODO: Fetch properties from sb and call recommender
                result = {"message": "Recommendations pending Supabase integration"}
        else:
            result = {"error": "Unknown function"}

        return result

    # Otherwise return normal LLM text
    return response.choices[0].message.get("content", "")
