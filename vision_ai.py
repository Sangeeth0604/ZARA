import os
import datetime
import pyautogui
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

VISION_MODELS = [
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.0-flash"
]

def analyze_screen(question="Analyze this screen. Explain what is visible in simple words. Keep it short and useful."):
    try:
        folder = "vision_screenshots"

        if not os.path.exists(folder):
            os.makedirs(folder)

        file_name = datetime.datetime.now().strftime("screen_%Y%m%d_%H%M%S.png")
        file_path = os.path.join(folder, file_name)

        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)

        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()

        prompt = f"""
You are ZARA Vision.

User question:
{question}

Analyze the screenshot and answer the user's question clearly.
Keep the answer short, practical, and easy to understand.
"""

        for model in VISION_MODELS:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=[
                        prompt,
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type="image/png"
                        )
                    ]
                )

                return response.text

            except Exception as e:
                print(f"Vision error with {model}:", e)

        return "Sorry Sangeeth, all vision models are busy or quota is exhausted."

    except Exception as e:
        return f"Vision error: {e}"