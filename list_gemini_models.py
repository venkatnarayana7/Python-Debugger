import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'backend/controller/.env'))
# Try looking in cwd too
load_dotenv('backend/controller/.env')

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("NO KEY")
    else:
        genai.configure(api_key=api_key)
        print("Listing models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
except Exception as e:
    print(e)
