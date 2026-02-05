import json
import boto3
import os

def lambda_handler(event, context):
    """
    Notifier Lambda (Lambda C).
    Triggered by Step Function final state.
    Payload expected:
    {
        "status": "completed",
        "original_request": { "code": "...", "connection_id": "..." },
        "results": [ ... ]
    }
    """
    print("Notifier triggered")
    
    # 1. Parse Event
    try:
        # Step Functions passes the result of the previous state
        payload = event
        
        # Extract connection info
        original_req = payload.get("original_request", {})
        connection_id = original_req.get("connection_id")
        
        if not connection_id:
            print("No connection_id found. Cannot push to WebSocket.")
            return {"status": "skipped", "reason": "no connection_id"}

        # 2. Upload to API Gateway
        domain_name = os.environ.get("WEBSOCKET_API_ENDPOINT", "https://example.com")
        # Ensure we have the full URL (https://xyz.execute-api.us-east-1.amazonaws.com/dev)
        
        apigw = boto3.client("apigatewaymanagementapi", endpoint_url=domain_name)
        
        # Send JSON
        apigw.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(payload).encode("utf-8")
        )
        print(f"Pushed result to {connection_id}")
        
        return {"status": "success"}

    except Exception as e:
        print(f"Notifier Error: {e}")
        # Identify gone connections
        if "GoneException" in str(e):
            print(f"Connection {connection_id} is gone.")
        
        return {"status": "failed", "error": str(e)}
