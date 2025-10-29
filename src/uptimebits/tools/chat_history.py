
from typing import Optional, List, Dict, Any
# from langchain.tools import tool
from strands import tool
from pydantic import BaseModel, Field
import json
import os
import boto3
from botocore.exceptions import ClientError
from langchain.tools.base import Tool
import re

# --- JSON Agent Input ---
class JSONAgentInput(BaseModel):
    question: str = Field(
        ...,
        description="The question content to log into chat history and to trigger the response"
    )
    message_id: Optional[str] = Field(
        None,
        description=(
            "Message identifier selecting which chat history file to use in S3. "
            "If not provided, a default chat history file will be used."
        ),
    )
    from_station: Optional[str] = Field(
        None, description="Origin station (if applicable)"
    )
    to_station: Optional[str] = Field(
        None, description="Destination station (if applicable)"
    )

# --- Helpers for S3 ---
def _get_bucket_and_key(message_id: Optional[str]) -> tuple[str, str]:
    bucket_name = os.environ.get("CHAT_HISTORY_BUCKET", "chathistorybucket-chatbuddy")
    key = f"chat-history/{message_id}.json" if message_id else "chat-history/default.json"
    return bucket_name, key

def _load_history_from_s3(s3_client, bucket: str, key: str) -> List[Dict[str, Any]]:
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read().decode("utf-8")
        data = json.loads(body)
        if isinstance(data, list):
            return data
        return []  # fallback if structure is wrong
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code in ("NoSuchKey", "404"):
            return []
        raise

def _save_history_to_s3(s3_client, bucket: str, key: str, history: List[Dict[str, Any]]) -> None:
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(history, ensure_ascii=False, indent=2).encode("utf-8"),
        ContentType="application/json",
    )

# --- Public Functions ---
def load_chat(message_id: Optional[str]) -> List[Dict[str, Any]]:
    """Load chat history from S3. Returns [] if not exists."""
    s3_client = boto3.client("s3")
    bucket, key = _get_bucket_and_key(message_id)
    return _load_history_from_s3(s3_client, bucket, key)

def save_chat(message_id: Optional[str], history: List[Dict[str, Any]]) -> None:
    """Save chat history to S3."""
    s3_client = boto3.client("s3")
    bucket, key = _get_bucket_and_key(message_id)
    _save_history_to_s3(s3_client, bucket, key, history)

def strip_html_tags(text: str) -> str:
    """Remove <b>, <br>, <ul>, etc. from stored Q/A HTML for clean context."""
    if not text:
        return ""
    return re.sub(r"<.*?>", "", text).strip()

def is_travel_related_query(question: str) -> bool:
    """
    Check if the question is related to travel/transport.
    Returns True for travel-related queries, False for irrelevant ones.
    """
    question_lower = question.lower()
    
    # Travel-related keywords
    travel_keywords = [
        'train', 'trains', 'station', 'stations', 'departure', 'arrival',
        'disruption', 'disruptions', 'delay', 'delays', 'timetable', 'schedule',
        'v/line', 'vline', 'metro', 'route', 'line', 'platform', 'journey',
        'travel', 'trip', 'service', 'services', 'transport', 'public transport',
        'ptv', 'myki', 'fare', 'ticket', 'cancel', 'cancelled', 'works', 'maintenance'
    ]
    
    # Check if any travel keywords are present
    has_travel_keywords = any(keyword in question_lower for keyword in travel_keywords)
    
    # Irrelevant keywords that override travel detection
    irrelevant_keywords = [
        'joke', 'weather', 'news', 'restaurant', 'food', 'movie', 'music',
        'sports', 'politics', 'celebrity', 'gossip', 'shopping', 'recipe',
        'game', 'entertainment', 'fashion', 'technology', 'science', 'history',
        'geography', 'math', 'homework', 'study', 'school', 'university'
    ]
    
    # Check if any irrelevant keywords are present
    has_irrelevant_keywords = any(keyword in question_lower for keyword in irrelevant_keywords)
    
    # If it has irrelevant keywords, it's not travel-related
    if has_irrelevant_keywords:
        return False
    
    # Context-based checks for follow-up questions
    context_indicators = [
        'disruption', 'delay', 'same route', 'that route', 'this route',
        'any problem', 'issues', 'status', 'update', 'current'
    ]
    
    has_context_indicators = any(indicator in question_lower for indicator in context_indicators)
    
    # Return True if has travel keywords OR context indicators (for follow-ups)
    return has_travel_keywords or has_context_indicators

# --- LangChain Tool (Logger with carry-forward) ---
@tool
def json_qa_tool(
    question: str,
    message_id: Optional[str] = None,
    from_station: Optional[str] = None,
    to_station: Optional[str] = None,
) -> str:
    """
    Tool for S3-backed chat history:
    - Only logs travel-related Q&A into S3
    - For irrelevant queries, returns context without storing the irrelevant question
    - Stores structured fields (from_station, to_station), carrying them forward if not provided
    - Returns the full chat history as JSON string (not HTML)
    """
    print(f"json_qa_tool received message_id: {message_id}")

    history = load_chat(message_id)
    
    # Check if the question is travel-related
    is_travel_query = is_travel_related_query(question)
    
    # --- Carry forward stations if missing (scan backwards) ---
    if history:
        for entry in reversed(history):
            if not from_station and entry.get("from_station"):
                from_station = entry["from_station"]
            if not to_station and entry.get("to_station"):
                to_station = entry["to_station"]
            if from_station and to_station:
                break

    # --- Only create and store entry if it's travel-related ---
    if is_travel_query:
        entry = {"question": question, "answer": ""}
        if from_station:
            entry["from_station"] = from_station
        if to_station:
            entry["to_station"] = to_station

        history.append(entry)
        save_chat(message_id, history)
        print(f"Stored travel-related query: {question}")
    else:
        print(f"Skipped storing irrelevant query: {question}")

    return json.dumps(history, ensure_ascii=False)


def make_json_qa_tool(message_id: str):
    """
    Tool that retrieves the latest relevant structured context
    (from_station, to_station, last Q/A) from chat history.
    Always returns the most recent carried-forward stations.
    Only considers travel-related entries for context.
    """

    def _json_qa_lookup(_: str = None):
        history = load_chat(message_id)
        if not history:
            return {}

        latest_question, latest_answer = None, None
        context = {}

        # dynamically collect all possible keys from history entries (excluding Q/A)
        possible_keys = set()
        for entry in history:
            possible_keys.update(k for k in entry.keys() if k not in ("question", "answer"))

        # scan backwards (latest → oldest), but only consider travel-related entries
        for entry in reversed(history):
            # Skip entries that don't look travel-related
            entry_question = entry.get("question", "")
            if entry_question and not is_travel_related_query(entry_question):
                continue
            
            # capture latest meaningful Q/A from travel-related entries
            if not latest_question and entry.get("question") and entry.get("answer"):
                latest_question = strip_html_tags(entry["question"])
                latest_answer = strip_html_tags(entry["answer"])

            # dynamically fill context (no hardcoded keys)
            for key in possible_keys:
                if key not in context or context[key] is None:
                    if key in entry and entry[key] is not None:
                        context[key] = entry[key]

            # stop early if we found everything
            if all(context.get(k) is not None for k in possible_keys) and latest_question and latest_answer:
                break

        return {
            **context,
            "latest_question": latest_question,
            "latest_answer": latest_answer,
        }

    return Tool(
        name="json_qa_tool",
        func=_json_qa_lookup,
        description=(
            "Fetches the most recent travel-related context from chat history. "
            "Skips irrelevant queries and returns JSON with keys: from_station, to_station, latest_question, latest_answer."
        )
    )