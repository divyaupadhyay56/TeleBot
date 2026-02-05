# ai_engine.py

import os
from google import genai

# -------------------------------
# Gemini Prompt Builder
# -------------------------------
def build_gemini_prompt(user_text, context, agent_type):
    base_rules = """
You are a medical support AI assistant.
You are NOT a doctor.

Strict rules:
- Do NOT diagnose any disease.
- Do NOT name or prescribe specific medicines.
- Do NOT give dosage instructions.
- Provide only general health guidance.
- Keep advice safe, non-alarming, and supportive.
- Always include a medical disclaimer.
"""

    if agent_type == "medical_ai":
        role_prompt = """
Task:
Analyze the user's symptoms and provide GENERAL medical guidance.

Response format:
1. Brief understanding of symptoms (1–2 lines)
2. General types of care or treatment doctors usually consider
3. Safety advice
4. When to consult a doctor

Tone:
- Calm
- Supportive
- Professional
"""

    elif agent_type == "home_remedy_ai":
        role_prompt = """
Task:
Provide general home care and wellness suggestions.

Response format:
1. General self-care tips
2. Lifestyle & rest suggestions
3. Safety disclaimer

Tone:
- Friendly
- Reassuring
- Simple
"""

    else:
        role_prompt = "Provide general health guidance only."

    return f"""
{base_rules}

Conversation context:
{context}

User symptoms:
{user_text}

{role_prompt}
"""


# -------------------------------
# Confidence Score Calculator
# -------------------------------
def calculate_confidence(text):
    keywords = [
        "pain", "ache", "fever", "cough", "cold",
        "headache", "tired", "fatigue", "nausea",
        "vomiting", "breathing", "weakness", "stress"
    ]

    text = text.lower()
    words = text.split()
    symptom_hits = sum(1 for k in keywords if k in text)

    score = 0.3  # base

    if len(words) > 5:
        score += 0.2
    if len(words) > 10:
        score += 0.2
    if symptom_hits >= 1:
        score += 0.2
    if symptom_hits >= 3:
        score += 0.1

    return round(min(score, 1.0), 2)


# -------------------------------
# Fallback (No Gemini Key)
# -------------------------------
def fallback_response(agent_type):
    if agent_type == "medical_ai":
        return {
            "reply": (
                "I can provide general health guidance.\n\n"
                "Based on your description, doctors usually focus on:\n"
                "- Managing discomfort\n"
                "- Supporting recovery through rest and hydration\n\n"
                "⚠️ Please consult a certified doctor for proper evaluation."
            ),
            "confidence_score": 0.4
        }

    if agent_type == "home_remedy_ai":
        return {
            "reply": (
                "🏡 General home care tips:\n"
                "- Stay hydrated\n"
                "- Get proper rest\n"
                "- Eat light and nutritious food\n"
                "- Manage stress and sleep well\n\n"
                "🌿 These tips support recovery but are not medical treatment."
            ),
            "confidence_score": 0.4
        }

    return {
        "reply": "Please describe your symptoms clearly.",
        "confidence_score": 0.3
    }


# -------------------------------
# MAIN AI FUNCTION
# -------------------------------
def analyze_symptoms(text, context, agent_type):
    api_key = os.getenv("GEMINI_API_KEY")

    # 🔹 If Gemini key missing → fallback
    if not api_key:
        return fallback_response(agent_type)

    try:
        client = genai.Client(api_key=api_key)

        prompt = build_gemini_prompt(text, context, agent_type)

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        ai_text = response.text.strip()
        confidence = calculate_confidence(text)

        return {
            "reply": ai_text,
            "confidence_score": confidence
        }

    except Exception as e:
        # Safety fallback
        return {
            "reply": "I faced an issue while analyzing your symptoms. Please try again.",
            "confidence_score": 0.3
        }
