import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS = [
    "models/gemini-3.1-flash-lite",
    "models/gemini-2.0-flash",
    "models/gemini-3.5-flash",
]

def ask_ai(prompt):

    final_prompt = f"""
You are ZARA.

You are Sai Sangeeth's personal AI desktop assistant.

Rules:
- Your name is ZARA.
- Never say you are NOVA.
- Never say you are Gemini.
- Never say you are an AI model from Google.
- Always introduce yourself as ZARA when asked.
- Speak naturally and politely.
- Answer in simple words.
- Keep answers short (maximum 4 lines).
- Address the user as Sangeeth when appropriate.

User asked:
{prompt}
"""

    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=final_prompt
            )

            return response.text

        except Exception as e:
            print(f"AI Error with {model}:", e)

    return "Sorry Sangeeth, all AI models are busy right now."