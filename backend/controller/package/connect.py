import json
import boto3
import os
import time

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME", "PVE_Connections")

def lambda_handler(event, context):
    """
    Handles $connect route.
    Saves connectionId and request metadata (e.g., source IP) to DynamoDB.
    """
    connection_id = event["requestContext"]["connectionId"]
    timestamp = int(time.time())
    
    # TTL: Auto-expire after 2 hours (2 * 3600)
    ttl = timestamp + 7200

    item = {
        "connectionId": connection_id,
        "timestamp": timestamp,
        "ttl": ttl,
        "status": "connected"
    }

    try:
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=item)
        print(f"Connected: {connection_id}")
        return {"statusCode": 200, "body": "Connected"}
    except Exception as e:
        print(f"Error connecting: {e}")
        return {"statusCode": 500, "body": "Failed to connect"}
