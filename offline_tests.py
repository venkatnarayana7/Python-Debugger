"""
Truth Engine - Offline Test Suite (No Network Required)
Tests security and sandbox components only
"""

import json
import os
import sys

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

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
# SECURITY TESTS
# ============================================================
def test_security_os_system():
    """Security: Block os.system calls"""
    malicious_code = "import os\nos.system('rm -rf /')"
    result = security.validate_code_safety(malicious_code)
    if result == True:
        return False, "CRITICAL: Malicious code was NOT blocked!"
    return True, "Blocked os.system successfully"

def test_security_subprocess():
    """Security: Block subprocess calls"""
    malicious_code = "import subprocess\nsubprocess.Popen(['cat', '/etc/passwd'])"
    result = security.validate_code_safety(malicious_code)
    if result == True:
        return False, "CRITICAL: subprocess.Popen was NOT blocked!"
    return True, "Blocked subprocess successfully"

def test_security_eval():
    """Security: Block eval() calls"""
    malicious_code = "user_input = 'test'\neval(user_input)"
    result = security.validate_code_safety(malicious_code)
    if result == True:
        return False, "CRITICAL: eval() was NOT blocked!"
    return True, "Blocked eval() successfully"

def test_security_exec():
    """Security: Block exec() calls"""
    malicious_code = "code = 'print(1)'\nexec(code)"
    result = security.validate_code_safety(malicious_code)
    if result == True:
        return False, "CRITICAL: exec() was NOT blocked!"
    return True, "Blocked exec() successfully"

def test_security_allow_safe():
    """Security: Allow legitimate safe code"""
    safe_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i))
"""
    result = security.validate_code_safety(safe_code)
    if result == False:
        return False, "Safe code was incorrectly blocked"
    return True, "Safe code allowed"

def test_security_allow_math():
    """Security: Allow math operations"""
    safe_code = """
import math
def calculate_area(radius):
    return math.pi * radius ** 2

areas = [calculate_area(r) for r in range(1, 11)]
print(sum(areas))
"""
    result = security.validate_code_safety(safe_code)
    if result == False:
        return False, "Math code was incorrectly blocked"
    return True, "Math code allowed"

# ============================================================
# SANDBOX TESTS
# ============================================================
def test_sandbox_valid_execution():
    """Sandbox: Execute valid code successfully"""
    candidate = "def multiply(a, b):\n    return a * b"
    test_script = "from fix import multiply\nresult = multiply(7, 6)\nassert result == 42\nprint('TEST PASSED')"
    
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

def test_sandbox_failing_test():
    """Sandbox: Detect failing test correctly"""
    candidate = "def add(a, b):\n    return a - b  # Bug"
    test_script = "from fix import add\nresult = add(2, 3)\nassert result == 5"
    
    event = {"candidate_code": candidate, "test_code": test_script}
    response = sandbox_app.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Unexpected status {response['statusCode']}"
    
    body = json.loads(response['body'])
    if body['return_code'] == 0:
        return False, "Expected test to FAIL but it passed"
    
    return True, f"Correctly detected failing test (exit code: {body['return_code']})"

def test_sandbox_security_block():
    """Sandbox: Block malicious code at entry"""
    malicious = "import os\nos.system('whoami')"
    test_script = "print('test')"
    
    event = {"candidate_code": malicious, "test_code": test_script}
    response = sandbox_app.lambda_handler(event, None)
    
    if response['statusCode'] != 403:
        return False, f"Expected 403, got {response['statusCode']}"
    
    return True, "Malicious code blocked with 403"

def test_sandbox_complex_code():
    """Sandbox: Execute complex algorithm"""
    candidate = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""
    test_script = """
from fix import quicksort
result = quicksort([3, 6, 8, 10, 1, 2, 1])
expected = [1, 1, 2, 3, 6, 8, 10]
assert result == expected, f"Got {result}"
print('QUICKSORT PASSED')
"""
    
    event = {"candidate_code": candidate, "test_code": test_script}
    response = sandbox_app.lambda_handler(event, None)
    
    if response['statusCode'] != 200:
        return False, f"Status {response['statusCode']}"
    
    body = json.loads(response['body'])
    if body['return_code'] != 0:
        return False, f"Return code {body['return_code']}: {body['stderr']}"
    
    return True, "Quicksort algorithm executed successfully"

# ============================================================
# MAIN
# ============================================================
def main():
    print("\n" + "="*70)
    print(" TRUTH ENGINE - OFFLINE TEST SUITE")
    print(" (Security + Sandbox Tests - No Network Required)")
    print("="*70)
    
    tests = [
        ("Security: Block os.system", test_security_os_system),
        ("Security: Block subprocess", test_security_subprocess),
        ("Security: Block eval()", test_security_eval),
        ("Security: Block exec()", test_security_exec),
        ("Security: Allow Safe Code", test_security_allow_safe),
        ("Security: Allow Math Code", test_security_allow_math),
        ("Sandbox: Valid Execution", test_sandbox_valid_execution),
        ("Sandbox: Failing Test", test_sandbox_failing_test),
        ("Sandbox: Security Block", test_sandbox_security_block),
        ("Sandbox: Complex Algorithm", test_sandbox_complex_code),
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
