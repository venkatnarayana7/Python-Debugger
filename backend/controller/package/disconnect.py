import boto3
import os

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME", "PVE_Connections")

def lambda_handler(event, context):
    """
    Handles $disconnect route.
    Removes connectionId from DynamoDB.
    """
    connection_id = event["requestContext"]["connectionId"]

    try:
        table = dynamodb.Table(TABLE_NAME)
        table.delete_item(Key={"connectionId": connection_id})
        print(f"Disconnected: {connection_id}")
        return {"statusCode": 200, "body": "Disconnected"}
    except Exception as e:
        print(f"Error disconnecting: {e}")
        return {"statusCode": 500, "body": "Failed to disconnect"}
