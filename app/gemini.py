import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Gemini API key not set.")
    print("⚠️ AI failed to generate an answer.")
    exit()

# Create client
client = genai.Client(api_key=api_key)

def generate_ai_answer(title, description):
    try:
        prompt = f"""
Question Title:
{title}

Description:
{description}

Give a helpful, expert-level answer.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        print("❌ Gemini API Error:", e)
        return "⚠️ AI failed to generate an answer."
