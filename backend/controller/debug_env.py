import os
from dotenv import load_dotenv

# Explicitly load
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

print(f"Loading from: {dotenv_path}")

keys = ["GEMINI_API_KEY", "GROQ_API_KEY", "DEEPSEEK_API_KEY"]
for k in keys:
    val = os.getenv(k)
    start = val[:4] if val else "NONE"
    length = len(val) if val else 0
    print(f"{k}: Start='{start}', Length={length}")
