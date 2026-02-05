import json
import os
from dotenv import load_dotenv
from main import lambda_handler

# Load environment variables from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def test_lambda():
    print("--- Starting Local Test ---")
    
    # Check for API Keys
    print(f"Gemini Key Present: {bool(os.getenv('GEMINI_API_KEY'))}")
    print(f"Groq Key Present: {bool(os.getenv('GROQ_API_KEY'))}")
    print(f"DeepSeek Key Present: {bool(os.getenv('DEEPSEEK_API_KEY'))}")

    # Mock Input
    mock_event = {
        "code": "def add(a, b):\n    return a + b\n\nprint(add(1, '2'))",
        "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    }

    print("\n--- Sending Payload ---")
    print(json.dumps(mock_event, indent=2))

    # Invoke Handler
    response = lambda_handler(mock_event, None)

    print("\n--- Response ---")
    print(json.dumps(response, indent=2))

    if response["statusCode"] == 200:
        body = json.loads(response["body"])
        print(f"\n[SUCCESS] Source: {body.get('source')}")
        print(f"Error Type: {body.get('error_type')}")
        print(f"Candidates Generated: {len(body['data']['candidates'])}")
    else:
        print("\n[FAILED]")

if __name__ == "__main__":
    test_lambda()
