import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from .schemas import FixPacket

load_dotenv()

def generate_fix_packet(code: str, error_log: str, error_type: str) -> dict:
    """
    Fallback: Generates fixes using DeepSeek V3 (via OpenAI client).
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("Missing DEEPSEEK_API_KEY")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    system_prompt = f"""
    You are the Truth Engine. The primary model failed. You are the safety net.
    Goal: Fix the user's broken code.
    Error Type: {error_type}

    Return a JSON object with this EXACT structure:
    {{
        "reproduction_script": "Standalone python script to reproduce the error",
        "candidates": ["Fix 1", "Fix 2", "Fix 3"]
    }}
    Do not use Markdown formatting in the response. Return raw JSON.
    """

    user_prompt = f"""
    Code:
    {code}

    Error:
    {error_log}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        json_response = json.loads(content)
        
        packet = FixPacket(**json_response)
        return packet.model_dump()
    except Exception as e:
        print(f"DeepSeek Fallback Error: {e}")
        # Last resort: Return empty structure to prevent total crash
        return {
            "reproduction_script": "# Failed to generate reproduction script",
            "candidates": ["# AI generation failed completely."]
        }
