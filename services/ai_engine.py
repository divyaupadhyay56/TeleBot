import os

def analyze_symptoms(text, context):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        # fallback AI (rule based)
        text = text.lower()
        if "fever" in text and "cough" in text:
            return "You may have flu-like symptoms. Please consult a doctor."
        if "headache" in text:
            return "Rest well and stay hydrated."
        return "Please describe your symptoms in more detail."

    # 🔥 If API key exists → Gemini LLM
    from google import genai
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"Context: {context}\nUser: {text}"
    )

    return response.text
