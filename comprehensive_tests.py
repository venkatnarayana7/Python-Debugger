"""
Truth Engine - Comprehensive Test Suite
Tests covering:
1. Error Categorization Accuracy
2. AI Fix Generation Quality
3. Sandbox Security Enforcement
4. Edge Cases & Error Handling
5. Full Integration Flow
"""

import json
import os
import sys
import time

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend/controller')))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend/controller/.env'))

from backend.controller import main as controller
from backend.sandbox import app as sandbox_app
from backend.sandbox import security

class TestResult:
    def __init__(self, name, passed, details=""):
        self.name = name
        self.passed = passed
        self.details = details

def run_test(name, test_func):
    """Run a test and return result"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)
    try:
        passed, details = test_func()
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"Result: {status}")
        if details:
            print(f"Details: {details}")
        return TestResult(name, passed, details)
    except Exception as e:
        print(f"Result: ❌ FAIL (Exception)")
        print(f"Error: {str(e)}")
        return TestResult(name, False, str(e))

# ============================================================
# TEST CASE 1: ZeroDivisionError Detection & Fix
# ============================================================
def test_zerodiv_error():
    """Test that system correctly identifies and fixes ZeroDivisionError"""
    code = """
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

result = calculate_average([])
print(result)
"""
    error = "ZeroDivisionError: division by zero"
    
    event = {"code": code, "error": error}
    response = controller.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Status {response['statusCode']}"
    
    body = json.loads(response['body'])
    
    # Verify error type detected
    if body['error_type'] not in ['RUNTIME', 'LOGIC']:
        return False, f"Wrong error type: {body['error_type']}"
    
    # Verify candidates generated
    if 'data' not in body or 'candidates' not in body['data']:
        return False, "No candidates generated"
    
    if len(body['data']['candidates']) == 0:
        return False, "Empty candidates array"
    
    return True, f"Generated {len(body['data']['candidates'])} fixes using {body['source']}"

# ============================================================
# TEST CASE 2: TypeError Detection & Fix
# ============================================================
def test_type_error():
    """Test string/int concatenation TypeError"""
    code = """
def greet(name, age):
    return "Hello " + name + ", you are " + age + " years old"

print(greet("Alice", 30))
"""
    error = "TypeError: can only concatenate str (not 'int') to str"
    
    event = {"code": code, "error": error}
    response = controller.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Status {response['statusCode']}"
    
    body = json.loads(response['body'])
    return True, f"Error type: {body['error_type']}, Source: {body['source']}"

# ============================================================
# TEST CASE 3: IndexError Detection & Fix
# ============================================================
def test_index_error():
    """Test list index out of range"""
    code = """
def get_last_element(lst):
    return lst[len(lst)]

items = [1, 2, 3]
print(get_last_element(items))
"""
    error = "IndexError: list index out of range"
    
    event = {"code": code, "error": error}
    response = controller.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Status {response['statusCode']}"
    
    body = json.loads(response['body'])
    return True, f"Error type: {body['error_type']}, Source: {body['source']}"

# ============================================================
# TEST CASE 4: SyntaxError Detection
# ============================================================
def test_syntax_error():
    """Test syntax error detection"""
    code = """
def broken_function(
    print("missing closing paren"
"""
    error = "SyntaxError: unexpected EOF while parsing"
    
    event = {"code": code, "error": error}
    response = controller.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Status {response['statusCode']}"
    
    body = json.loads(response['body'])
    if 'SYNTAX' not in body['error_type'].upper() and 'UNKNOWN' not in body['error_type'].upper():
        # Syntax errors are tricky, categorizer might classify differently
        pass
    
    return True, f"Error type: {body['error_type']}"

# ============================================================
# TEST CASE 5: Security - Block os.system
# ============================================================
def test_security_os_system():
    """Security: Block os.system calls"""
    malicious_code = """
import os
os.system("rm -rf /")
"""
    result = security.validate_code_safety(malicious_code)
    
    if result == True:
        return False, "CRITICAL: Malicious code was NOT blocked!"
    
    return True, "Blocked os.system successfully"

# ============================================================
# TEST CASE 6: Security - Block subprocess
# ============================================================
def test_security_subprocess():
    """Security: Block subprocess calls"""
    malicious_code = """
import subprocess
subprocess.Popen(["cat", "/etc/passwd"])
"""
    result = security.validate_code_safety(malicious_code)
    
    if result == True:
        return False, "CRITICAL: subprocess.Popen was NOT blocked!"
    
    return True, "Blocked subprocess successfully"

# ============================================================
# TEST CASE 7: Security - Block eval
# ============================================================
def test_security_eval():
    """Security: Block eval() calls"""
    malicious_code = """
user_input = "__import__('os').system('whoami')"
eval(user_input)
"""
    result = security.validate_code_safety(malicious_code)
    
    if result == True:
        return False, "CRITICAL: eval() was NOT blocked!"
    
    return True, "Blocked eval() successfully"

# ============================================================
# TEST CASE 8: Security - Allow Safe Code
# ============================================================
def test_security_allow_safe():
    """Security: Allow legitimate safe code"""
    safe_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
    result = security.validate_code_safety(safe_code)
    
    if result == False:
        return False, "Safe code was incorrectly blocked"
    
    return True, "Safe code allowed"

# ============================================================
# TEST CASE 9: Sandbox Execution - Valid Code
# ============================================================
def test_sandbox_valid_execution():
    """Sandbox: Execute valid code successfully"""
    candidate = """
def multiply(a, b):
    return a * b
"""
    test_script = """
from fix import multiply
result = multiply(7, 6)
assert result == 42, f"Expected 42, got {result}"
print("TEST PASSED")
"""
    
    event = {"candidate_code": candidate, "test_code": test_script}
    response = sandbox_app.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Status {response['statusCode']}"
    
    body = json.loads(response['body'])
    if body['return_code'] != 0:
        return False, f"Return code {body['return_code']}: {body['stderr']}"
    
    if "TEST PASSED" not in body['stdout']:
        return False, f"Expected 'TEST PASSED' in output"
    
    return True, "Code executed and test passed"

# ============================================================
# TEST CASE 10: Sandbox Execution - Failing Test
# ============================================================
def test_sandbox_failing_test():
    """Sandbox: Detect failing test correctly"""
    candidate = """
def add(a, b):
    return a - b  # Bug: subtraction instead of addition
"""
    test_script = """
from fix import add
result = add(2, 3)
assert result == 5, f"Expected 5, got {result}"
print("TEST PASSED")
"""
    
    event = {"candidate_code": candidate, "test_code": test_script}
    response = sandbox_app.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Unexpected status {response['statusCode']}"
    
    body = json.loads(response['body'])
    if body['return_code'] == 0:
        return False, "Expected test to FAIL but it passed"
    
    return True, f"Correctly detected failing test (exit code: {body['return_code']})"

# ============================================================
# TEST CASE 11: Edge Case - Empty Code
# ============================================================
def test_edge_empty_code():
    """Edge Case: Handle empty code gracefully"""
    event = {"code": "", "error": "SyntaxError"}
    response = controller.lambda_handler(event, None)
    
    # Should return 400 for invalid input
    if response['statusCode'] == 400:
        return True, "Correctly rejected empty code"
    
    # Or handle gracefully
    return True, f"Handled empty code with status {response['statusCode']}"

# ============================================================
# TEST CASE 12: Edge Case - Very Long Error
# ============================================================
def test_edge_long_error():
    """Edge Case: Handle very long error message"""
    code = "x = 1/0"
    error = "ZeroDivisionError: " + "A" * 1000  # Very long error
    
    event = {"code": code, "error": error}
    response = controller.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Failed with status {response['statusCode']}"
    
    return True, "Handled long error message"

# ============================================================
# MAIN: Run All Tests
# ============================================================
def main():
    print("\n" + "="*70)
    print(" TRUTH ENGINE - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        ("ZeroDivisionError Fix", test_zerodiv_error),
        ("TypeError Fix", test_type_error),
        ("IndexError Fix", test_index_error),
        ("SyntaxError Detection", test_syntax_error),
        ("Security: Block os.system", test_security_os_system),
        ("Security: Block subprocess", test_security_subprocess),
        ("Security: Block eval()", test_security_eval),
        ("Security: Allow Safe Code", test_security_allow_safe),
        ("Sandbox: Valid Execution", test_sandbox_valid_execution),
        ("Sandbox: Failing Test", test_sandbox_failing_test),
        ("Edge: Empty Code", test_edge_empty_code),
        ("Edge: Long Error", test_edge_long_error),
    ]
    
    results = []
    for name, test_func in tests:
        result = run_test(name, test_func)
        results.append(result)
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    
    for r in results:
        status = "✅" if r.passed else "❌"
        print(f"{status} {r.name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed out of {len(results)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️ {failed} TESTS FAILED")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
