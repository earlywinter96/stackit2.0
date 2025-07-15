# app/gemini.py
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Gemini API key not set.")
    print("⚠️ AI failed to generate an answer.")
    exit()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_ai_answer(title, description):
    try:
        prompt = f"Question Title: {title}\n\nDescription: {description}\n\nGive a helpful, expert-level answer."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini API Error:", e)
        return "⚠️ AI failed to generate an answer."
    
