import json
from sandbox import security, runner

def lambda_handler(event, context):
    """
    AWS Lambda Handler for Sandbox Execution.
    Expected Payload: { "candidate_code": "...", "test_code": "..." }
    """
    print("Received sandbox request")
    
    # Parse input
    # If invoked via API Gateway, body might be string
    if "body" in event:
        try:
            body = json.loads(event["body"])
        except:
            body = event # Fallback
    else:
        body = event

    candidate = body.get("candidate_code")
    test_script = body.get("test_code")

    if not candidate or not test_script:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'candidate_code' or 'test_code'"})
        }

    # 1. Security Check
    if not security.validate_code_safety(candidate):
        return {
            "statusCode": 403,
            "body": json.dumps({
                "error": "Security Violation",
                "details": "Code contains banned keywords (os, subprocess, eval, etc.)"
            })
        }

    # 2. Execution
    result = runner.execute_verification(candidate, test_script)

    # 3. Response
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
