import os
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def test_groq():
    print("\n--- Testing Groq ---")
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hi"}],
            model="llama3-8b-8192",
            max_tokens=1
        )
        print("Success!")
    except Exception as e:
        print(f"FAILED: {e}")

def test_gemini():
    print("\n--- Testing Gemini ---")
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Hi")
        print("Success!")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_groq()
    test_gemini()
