import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from .schemas import FixPacket

load_dotenv()

def generate_fix_packet(code: str, error_log: str, error_type: str) -> dict:
    """
    Generates a reproduction script and 3 candidate fixes using Gemini 1.5 Flash.
    Returns a dictionary matching the FixPacket schema.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY")

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.2,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config=generation_config,
    )

    system_prompt = f"""
    You are the Truth Engine, a high-reliability Python repair system.
    Goal: Fix the user's broken code based on the provided error log.
    Error Type: {error_type}

    You must return a JSON object with this EXACT structure:
    {{
        "reproduction_script": "A standalone Python script that reproduces the error. It must fail with the same error type.",
        "candidates": [
            "Candidate Fix 1 (Full Code)",
            "Candidate Fix 2 (Alternative Approach)",
            "Candidate Fix 3 (Defensive/Robust Approach)"
        ]
    }}

    Rules:
    1. The reproduction script must be self-contained (mock data if needed).
    2. Candidate fixes must be the FULL file content, not just diffs.
    3. Do not use Markdown backticks in the JSON string values.
    """

    user_prompt = f"""
    Broken Code:
    {code}

    Error Log:
    {error_log}
    """

    try:
        response = model.generate_content([system_prompt, user_prompt])
        json_response = json.loads(response.text)
        # Validate with Pydantic
        packet = FixPacket(**json_response)
        return packet.model_dump()
    except Exception as e:
        print(f"Gemini Brain Error: {e}")
        raise e
