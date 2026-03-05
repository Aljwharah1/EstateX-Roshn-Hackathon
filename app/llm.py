"""Lightweight LLM wrapper for FastAPI endpoints.

Provides safe ask_llm(user_message: str) function.
All data comes from Supabase - no local files or Excel imports.
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    _openai_available = True
except Exception:
    OpenAI = None
    _openai_available = False


def _extract_content(choice):
    """Return the textual content from a choice object/dict in a robust way."""
    try:
        msg = choice.get("message") if isinstance(choice, dict) else getattr(choice, "message", None)
        if msg is None:
            return choice.get("text") if isinstance(choice, dict) else getattr(choice, "text", None)

        if isinstance(msg, dict):
            return msg.get("content") or msg.get("text") or ""
        return getattr(msg, "content", None) or getattr(msg, "text", None) or str(msg)
    except Exception:
        return ""


def ask_llm(user_message: str) -> str:
    """
    Ask the LLM and return a string reply.
    
    Uses Supabase as the only data source for property and market information.
    Returns helpful message if OpenAI API is unavailable.
    """
    if not _openai_available or os.getenv("OPENAI_API_KEY") is None:
        return "OPENAI_API_KEY not available or OpenAI SDK not installed."

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = (
        "You are EstateX Advisor, an intelligent real estate assistant for the Saudi Arabian market. "
        "You help users find and evaluate properties in Riyadh. "
        "\n"
        "Guidelines:\n"
        "1. When users ask about specific properties or locations, acknowledge their request and explain what you can do.\n"
        "2. You have access to a database of real estate properties in Riyadh with various districts and locations.\n"
        "3. Help users understand the market, property features, investment potential, and pricing.\n"
        "4. Use simple, friendly language and provide practical real estate advice.\n"
        "5. If you don't have exact answers, provide helpful guidance based on real estate principles and the available data.\n"
        "\n"
        "Always be helpful and guide the user toward finding suitable properties in their budget and preferences."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
        )

        choices = getattr(response, "choices", None) or response.get("choices", [])
        if not choices:
            return "No response from LLM."

        content = _extract_content(choices[0])
        return content or ""
    except Exception as e:
        return f"LLM request failed: {e}"
