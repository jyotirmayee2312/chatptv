import json
import boto3
import uuid
import os
from botocore.exceptions import ClientError

from agent.agent_executor import agent_executor
from context.conversation import context

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("CHAT_HISTORY_BUCKET", "chathistorybucket-chatbuddy")
def save_chat_to_s3(messageid, question, answer):
    messageid = messageid or "default"
    key = f"chat-history/{messageid}.json"

    new_entry = {
        "question": question,
        "answer": answer
    }

    try:
        existing_obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        existing_data = json.loads(existing_obj["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            existing_data = []  # File does not exist yet
        else:
            print(f"Error reading S3 file: {e}")
            existing_data = []

    existing_data.append(new_entry)

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(existing_data),
        ContentType="application/json"
    )

    return key


def lambda_handler(event, context):
    body = json.loads(event["body"])
    user_input = body.get("question", "")
    messageid = body.get("messageid")  # <-- Get messageid from API request

    response = agent_executor.invoke({"input": user_input})

    # Extract answer
    answer_html = ""
    if isinstance(response.get("output"), list) and len(response["output"]) > 0:
        answer_html = response["output"][0].get("text", "")
    elif isinstance(response.get("output"), str):
        answer_html = response["output"]

    # Save chat history using messageid as filename
    save_chat_to_s3(messageid, user_input, answer_html)

    frontend_payload = {
        "status_code": 200,
        "status": True,
        "message": "Message sent",
        "data": {
            "conversation": [
                {
                    "messageid": messageid,  # send back the same messageid
                    "session_id": None,
                    "question": user_input,
                    "answer": answer_html,
                    "errormsg": None,
                    "quickReplies": None
                }
            ]
        }
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps(frontend_payload),
    }
