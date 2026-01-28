import os
from google import genai

# ✅ Create client safely
def _get_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def analyze_symptoms(text, context=None):
    """
    Gemini LLM-based medical assistant (safe + short responses)
    """

    client = _get_client()
    if client is None:
        return "Gemini API key missing. Please set GEMINI_API_KEY to enable AI responses."

    if not text:
        return "Please describe your symptoms."

    prompt = f"""
You are a medical assistant.
Give safe, short, non-alarming guidance.
If symptoms seem severe, advise urgent doctor visit.

Conversation context:
{context}

User message:
{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        return f"AI service error: {str(e)}"
