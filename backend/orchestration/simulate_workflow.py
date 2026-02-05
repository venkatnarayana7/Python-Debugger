import json
import os
import sys
import time

# Setup Paths to import sibling modules
# Setup Paths to import sibling modules and mimic Lambda environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))) # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../controller'))) # For 'ag'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # For 'sandbox' (via backend.sandbox or just sandbox if folder matches)

# NOTE: The Sandbox app Expects 'from sandbox import ...'
# This implies 'sandbox' is a direct child of a path in sys.path.
# We added '..' (backend/orchestration/.. -> backend).
# So 'import sandbox' should work if 'backend/sandbox' has __init__.py

from backend.controller import main as controller_main
from backend.sandbox import app as sandbox_app
from dotenv import load_dotenv

# Load env for controller
load_dotenv(os.path.join(os.path.dirname(__file__), '../controller/.env'))

def simulate_full_flow():
    print("\n=== TRUTH ENGINE: ORCHESTRATION SIMULATION ===\n")

    # 1. INPUT: A Broken Piece of Code
    broken_code = """
def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print(calculate_average([]))
"""
    error_log = "ZeroDivisionError: division by zero"

    print("--- [Step 1] Triggering Controller (The Brain) ---")
    controller_event = {
        "code": broken_code,
        "error": error_log
    }
    
    t0 = time.time()
    controller_response = controller_main.lambda_handler(controller_event, None)
    t1 = time.time()
    
    if controller_response['statusCode'] != 200:
        print(f"CRITICAL: Controller failed: {controller_response}")
        return

    brain_output = json.loads(controller_response['body'])
    print(f"Brain Execution Time: {t1-t0:.2f}s")
    print(f"Source: {brain_output['source']}")
    print(f"Error Type: {brain_output['error_type']}")
    
    data = brain_output['data']
    reproduction_script = data['reproduction_script']
    candidates = data['candidates']
    
    print(f"\nGenerated {len(candidates)} Candidates.")
    # print(f"Reproduction Script Preview:\n{reproduction_script[:100]}...")

    # 2. FAN-OUT: Run Sandbox for each candidate
    print("\n--- [Step 2] Fan-Out Execution (The Body) ---")
    
    results = []
    
    for i, candidate in enumerate(candidates):
        print(f"\n> Running Candidate {i+1}...")
        
        sandbox_event = {
            "candidate_code": candidate,
            "test_code": reproduction_script
        }
        
        t_start = time.time()
        sandbox_response = sandbox_app.lambda_handler(sandbox_event, None)
        t_end = time.time()
        
        if sandbox_response['statusCode'] == 200:
            result_body = json.loads(sandbox_response['body'])
            return_code = result_body['return_code']
            status = "PASS" if return_code == 0 else "FAIL"
            print(f"  Result: [{status}] (Exit Code: {return_code})")
            print(f"  Duration: {t_end - t_start:.2f}s")
            if status == "FAIL":
                print(f"  Stderr: {result_body['stderr'].strip()[:200]}")
            
            results.append({
                "candidate_id": i+1,
                "status": status,
                "duration": t_end - t_start,
                "details": result_body
            })
        else:
            print(f"  Result: [SYSTEM ERROR] {sandbox_response['statusCode']}")

    # 3. AGGREGATION
    print("\n--- [Step 3] Final Results ---")
    winning_fixes = [r for r in results if r['status'] == "PASS"]
    
    if winning_fixes:
        winner = min(winning_fixes, key=lambda x: x['duration'])
        print(f"WINNER: Candidate {winner['candidate_id']} ({winner['duration']:.2f}s)")
    else:
        print("NO FIX FOUND. All candidates failed.")

if __name__ == "__main__":
    simulate_full_flow()
