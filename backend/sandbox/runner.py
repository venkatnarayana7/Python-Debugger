import subprocess
import os
import sys

def execute_verification(candidate_code: str, test_code: str, timeout: int = 5) -> dict:
    """
    Writes code to /tmp and executes the test script in a subprocess.
    Returns dictionary with return_code, stdout, stderr.
    """
    tmp_dir = "/tmp"
    
    # On Windows (Local Testing), use a local temp dir if /tmp doesn't exist
    if sys.platform == "win32":
        tmp_dir = os.path.join(os.getcwd(), "temp_sandbox")
        os.makedirs(tmp_dir, exist_ok=True)

    fix_path = os.path.join(tmp_dir, "fix.py")
    test_path = os.path.join(tmp_dir, "test.py")

    try:
        # Write files
        with open(fix_path, "w") as f:
            f.write(candidate_code)
        
        with open(test_path, "w") as f:
            f.write(test_code)

        # Execute
        # We need to ensure the subprocess can find 'fix.py' in the same directory
        env = os.environ.copy()
        env["PYTHONPATH"] = tmp_dir
        
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=tmp_dir # execute from the temp dir
        )

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "return_code": 124, # Standard timeout exit code
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds."
        }
    except Exception as e:
        return {
            "return_code": 1,
            "stdout": "",
            "stderr": f"Sandbox Internal Error: {str(e)}"
        }
