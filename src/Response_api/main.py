import json
import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("CHAT_HISTORY_BUCKET", "chathistorybucket-chatbuddy")

def lambda_handler(event, context):
    # Expect messageid in query params or request body
    messageid = None

    # Try to get messageid from query string parameters
    if event.get("queryStringParameters"):
        messageid = event["queryStringParameters"].get("messageid")

    # Or from POST body if needed
    if not messageid and event.get("body"):
        try:
            body = json.loads(event["body"])
            messageid = body.get("messageid")
        except Exception:
            pass

    if not messageid:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "messageid parameter is required"})
        }

    key = f"chat-history/{messageid}.json"

    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        data = json.loads(obj["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            data = []  # No chat history yet
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"message": f"Error reading chat history: {str(e)}"})
            }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "messageid": messageid,
            "conversation": data
        })
    }
