import json
from ag import categorizer, brain, fallback

def lambda_handler(event, context):
    """
    AWS Lambda Handler for Truth Engine Controller.
    Expected Payload: { "code": "...", "error": "..." }
    """
    try:
        # Parse body (API Gateway can pass body as string)
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        code = body.get("code")
        error_log = body.get("error")
        connection_id = body.get("connection_id")  # For WebSocket passthrough

        if not code or not error_log:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'code' or 'error' field"})
            }

        # Step 1: Categorize
        print("Categorizing error...")
        error_type = categorizer.classify_error(code, error_log)
        print(f"Error classified as: {error_type}")

        # Step 2: Generate Fix (Brain -> Fallback)
        try:
            print("Attempting generation with Gemini...")
            result = brain.generate_fix_packet(code, error_log, error_type)
            source = "Gemini 1.5 Flash"
        except Exception as e:
            print(f"Gemini failed: {e}. Switching to DeepSeek...")
            try:
                result = fallback.generate_fix_packet(code, error_log, error_type)
                source = "DeepSeek V3"
            except Exception as e2:
                print(f"DeepSeek failed: {e2}")
                return {
                    "statusCode": 500,
                    "body": json.dumps({"error": "All AI models failed to generate a fix."})
                }

        # Step 3: Return Response
        response_payload = {
            "status": "success",
            "source": source,
            "error_type": error_type,
            "connection_id": connection_id,  # Preserve for downstream
            "data": result
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response_payload)
        }

    except Exception as e:
        print(f"Critical Lambda Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
