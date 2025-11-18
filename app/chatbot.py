# app/chatbot.py
import os
import openai
from typing import Dict, Any, List

openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")  # change if needed

# System instruction template that strictly limits the LLM to provided inputs
SYSTEM_PROMPT = """
You are EstateX Assistant. You MUST ONLY use the information explicitly provided to you
in this conversation (data snippets, recommender outputs, and the XGBoost forecasts).
Do NOT use external knowledge, the internet, or any other source. Do not hallucinate.
Answer concisely, cite the provided source block names (e.g., [RECOMMENDER], [FORECAST], [DATA_SUMMARY])
when you base statements on them, and clearly say "No more data available" if asked for information not in the provided blocks.
Be factual, short, and give actionable next steps where appropriate.
If asked to provide a recommendation beyond the provided data, say you cannot and suggest what extra data is needed.
Always use temperature=0 behavior (deterministic).
"""

def build_context(recs: List[Dict[str,Any]], forecasts: List[Dict[str,Any]], data_summary: Dict[str,Any]) -> str:
    """
    Build a compact context string with labeled blocks that will be fed to the LLM.
    Keep the context short and factual. The model will be explicitly told to use only these blocks.
    """
    lines = []
    # Data summary block
    lines.append("[DATA_SUMMARY]")
    for k, v in data_summary.items():
        lines.append(f"{k}: {v}")

    # Recommender outputs block (top N recommendations)
    lines.append("\n[RECOMMENDER]")
    if not recs:
        lines.append("NO_RECOMMENDATIONS")
    else:
        for i, r in enumerate(recs[:10], 1):
            # include only key fields to limit prompt length
            district = r.get("district")
            price = r.get("price_sar")
            area = r.get("area_sqm")
            ppm = r.get("price_per_sqm")
            score = r.get("score", None)
            lines.append(f"{i}. district={district} | price={price} | area_sqm={area} | price_per_sqm={ppm} | score={score}")

    # Forecasts block (for top candidates)
    lines.append("\n[FORECAST]")
    if not forecasts:
        lines.append("NO_FORECASTS")
    else:
        for f in forecasts:
            # include minimal forecast info
            lines.append(f"- transaction_id={f.get('transaction_id', 'NA')} | predicted_change={f.get('predicted_change', 'NA')}")

    return "\n".join(lines)

def generate_reply(user_question: str, recommender_output: List[Dict[str,Any]], forecasts: List[Dict[str,Any]], data_summary: Dict[str,Any]) -> str:
    """
    Call OpenAI ChatCompletion with deterministic settings (temperature=0) and a prompt
    that contains only the provided context blocks.
    """
    if openai.api_key is None:
        raise RuntimeError("OPENAI_API_KEY is not set in environment")

    context = build_context(recommender_output, forecasts, data_summary)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nUser question: {user_question}\n\nTask: Answer using ONLY the information in the Context blocks. Be concise. If you need more data to answer, say exactly what data is missing."}
    ]

    resp = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.0,
        max_tokens=400,
        n=1
    )

    text = resp["choices"][0]["message"]["content"].strip()
    return text
