import json
import os
import sys

# Ensure we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.sandbox import app

def test_safe_execution():
    print("\n--- Test 1: Safe Execution ---")
    candidate = """
def add(a, b):
    return a + b
"""
    test_script = """
from fix import add
print(f"Result: {add(2, 3)}") # Expect 5
"""
    
    event = {
        "candidate_code": candidate,
        "test_code": test_script
    }
    
    response = app.lambda_handler(event, None)
    print(f"Status: {response['statusCode']}")
    body = json.loads(response['body'])
    print(f"Output: {body.get('stdout')}")
    print(f"Stderr: {body.get('stderr')}")
    
    if "Result: 5" in body.get('stdout', ''):
        print("PASS")
    else:
        print("FAIL")

def test_unsafe_execution():
    print("\n--- Test 2: Unsafe Execution (Security Block) ---")
    candidate = """
import os
os.system("echo hacked")
"""
    test_script = "print('Should not run')"
    
    event = {
        "candidate_code": candidate,
        "test_code": test_script
    }
    
    response = app.lambda_handler(event, None)
    print(f"Status: {response['statusCode']}")
    
    if response['statusCode'] == 403:
        print("PASS (Blocked)")
    else:
        print(f"FAIL (Allowed with status {response['statusCode']})")

if __name__ == "__main__":
    test_safe_execution()
    test_unsafe_execution()
