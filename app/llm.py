# app/llm.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from .recommender import RuleBasedRecommender
from .model import PriceForecaster
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load your dataset and models once (fast)
DATA_PATH = "data/Finalized_Data.xlsx"
df = pd.read_excel(DATA_PATH)

recommender = RuleBasedRecommender(df)
forecaster = PriceForecaster("models/xgb_model.json")

def ask_llm(user_message: str):
    """
    The LLM is NOT allowed to hallucinate or use external knowledge.
    It can ONLY answer using:
      - the dataset
      - the rule-based recommender
      - the trained XGBoost model
    """

    system_prompt = """
    You are an assistant for a Riyadh real estate investment platform.
    You MUST use only the following sources when responding:
    - the dataset provided (Riyadh transactions with columns: region, city, property_class, ... etc.)
    - the rule-based recommender system
    - the XGBoost forecasting model
    
    You are NOT allowed to bring external information.
    You are NOT allowed to hallucinate.
    If the dataset or models do not contain the required information, answer:
    "This information is not available in the system."
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message["content"]
