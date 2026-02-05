import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def classify_error(code: str, error_log: str) -> str:
    """
    Classifies the error into one of: SYNTAX, LOGIC, RUNTIME, SECURITY.
    Uses Groq (Llama 3) for fast inference.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "UNKNOWN (Missing API Key)"

    client = Groq(api_key=api_key)

    prompt = f"""
    You are a Senior Python Debugger.
    Analyze the following Code and Error Log.
    Classify the error into exactly one of these categories:
    - SYNTAX (IndentationError, SyntaxError, etc.)
    - LOGIC (Wrong output, infinite loop, business logic fail)
    - RUNTIME (IndexError, TypeError, keyError, etc.)
    - SECURITY (Usage of os.system, eval, etc.)

    Code:
    ```python
    {code}
    ```

    Error:
    {error_log}

    Return ONLY the category name (e.g., "SYNTAX"). Do not add any explanation.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=10,
        )
        return chat_completion.choices[0].message.content.strip().upper()
    except Exception as e:
        print(f"Categorizer Error: {e}")
        return "UNKNOWN"
