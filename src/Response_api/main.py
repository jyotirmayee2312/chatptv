import json
import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("CHAT_HISTORY_BUCKET", "chathistorybucket-chatbuddy")

def lambda_handler(event, context):
    messageid = None

    # Get messageid from query string
    if event.get("queryStringParameters"):
        messageid = event["queryStringParameters"].get("messageid")

    # Or from body
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
    print("key",key)

    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        data = json.loads(obj["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            data = []
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"message": f"Error reading chat history: {str(e)}"})
            }

    # ✅ Wrap in desired format
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "status_code": 200,
            "status": True,
            "message": "History received",
            "data": {
                "messageid": messageid,
                "conversation": data
            }
        })
    }

