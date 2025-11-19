"""Lightweight LLM wrapper used by the FastAPI endpoints.

Provides a safe `ask_llm(user_message: str)` function. The implementation
handles different shapes returned by various OpenAI SDK versions and
fails gracefully when the API key is missing.
"""
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

try:
    # Import OpenAI client lazily so module import doesn't fail if package missing
    from openai import OpenAI
    _openai_available = True
except Exception:
    OpenAI = None
    _openai_available = False

# Local model/recommender imports (these are lightweight wrappers)
from .recommender import RuleBasedRecommender
from .model import ForecastModel

# Initialize dataset and engines (best-effort)
DATA_PATH = "data/Finalized_Data.xlsx"
try:
    df = pd.read_excel(DATA_PATH)
except Exception:
    df = pd.DataFrame()

recommender = RuleBasedRecommender(df)
forecaster = ForecastModel("models/xgb_model.json", "models/encoders.pkl")


def _extract_content(choice):
    """Return the textual content from a choice object/dict in a robust way."""
    # choice may be dict-like or object-like depending on SDK
    try:
        msg = choice.get("message") if isinstance(choice, dict) else getattr(choice, "message", None)
        if msg is None:
            # Older shape: 'text' field
            return choice.get("text") if isinstance(choice, dict) else getattr(choice, "text", None)

        # message may be dict or object
        if isinstance(msg, dict):
            return msg.get("content") or msg.get("text") or ""
        # object-like
        return getattr(msg, "content", None) or getattr(msg, "text", None) or str(msg)
    except Exception:
        return ""


def ask_llm(user_message: str) -> str:
    """Ask the LLM and return a string reply.

    If OpenAI SDK/key isn't available, return a helpful message rather than
    raising an exception so the API endpoint can respond gracefully.
    """
    # Quick checks
    if not _openai_available or os.getenv("OPENAI_API_KEY") is None:
        return "OPENAI_API_KEY not available or OpenAI SDK not installed."

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = (
        "You are EstateX Advisor's assistant. Use only the internal dataset, the "
        "rule-based recommender, and the XGBoost model. If asked for anything "
        "outside these sources, reply: 'This information is not available in the system.'"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
        )

        # Choose first choice robustly
        choices = getattr(response, "choices", None) or response.get("choices", [])
        if not choices:
            return "No response from LLM."

        content = _extract_content(choices[0])
        return content or ""
    except Exception as e:
        return f"LLM request failed: {e}"
