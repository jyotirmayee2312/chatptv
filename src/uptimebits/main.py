import json
from datetime import datetime, timezone
import os
from functions.datetime_parser import (
    parse_natural_datetime,
    get_melbourne_date_string,
    get_melbourne_time_string,
)
from dotenv import load_dotenv

load_dotenv()


os.environ["AWS_ACCESS_KEY_ID"]=os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"]=os.getenv("AWS_SECRET_ACCESS_KEY")
os.environ["AWS_DEFAULT_REGION"]=os.getenv("AWS_DEFAULT_REGION")
os.environ["CHAT_HISTORY_BUCKET"]=os.getenv("CHAT_HISTORY_BUCKET")
from Memory import MemoryManager
from Memory_hook import MemoryHookProvider
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from Context import app_context
from agent.agent_executor import create_agent_with_tools
from tools.chat_history import load_chat, save_chat, make_json_qa_tool
from agent.tool_router import tools as all_tools
memoryManager= MemoryManager()
Memory_name="chatvtv_memory"

memoryManager.create_memory()
client=memoryManager.get_client()
memory_id=memoryManager.get_memory_id()
print("Memory_id : ",memory_id)

agent_hook= MemoryHookProvider(client,memory_id)
session_id=app_context.session_id
actor_id= app_context.actor_id


def lambda_handler(event, _):
    body = json.loads(event["body"])
    user_input = body.get("question", "")
    message_id = body.get("messageid")
    session_id= message_id
    actor_id= message_id
    app_context.session_id=session_id
    app_context.actor_id=actor_id
    print("messageid", message_id)

    # --- Parse date/time from user query (Melbourne timezone) ---
    parsed_date, parsed_time = parse_natural_datetime(user_input)
    if not parsed_date:
        parsed_date = get_melbourne_date_string()
    if not parsed_time:
        parsed_time = get_melbourne_time_string()

    print(f"[main.py] Parsed datetime → date={parsed_date}, time={parsed_time}")

    # --- Load/create chat history ---
    chat_history = load_chat(message_id)
    if not chat_history:
        print(f"No existing chat history for {message_id}. Creating new history.")
        save_chat(message_id, [])

    # --- Bind session-scoped json_qa_tool ---
    bound_json_tool = make_json_qa_tool(message_id)
    bound_tools = []
    for t in all_tools:
        if getattr(t, "name", "") == "json_qa_tool":
            bound_tools.append(bound_json_tool)
        else:
            bound_tools.append(t)

    # --- Build agent with bound tools ---
    agent_executor_with_history = create_agent_with_tools(bound_tools,session_id,actor_id,agent_hook)

    # --- Make a tagged user input so LLM/tools always "see" parsed datetime ---
    # Example: "can I take a train tomorrow at 10am\n[PARSED_DATE=2025-09-16][PARSED_TIME=10:00 AM]"
    user_input_with_dt = f"{user_input}\n[PARSED_DATE={parsed_date}][PARSED_TIME={parsed_time}]"

    # --- Invoke agent: pass both structured fields AND the tagged input ---
    # (Some tool calls will be produced by LLM; passing date/time explicitly
    #  as keys increases the chance LangChain's tool arg population includes them.)
    invoke_payload = {
        "input": user_input_with_dt,   # LLM sees the tags
        "raw_input": user_input,       # keep original user text too (optional)
        "date": parsed_date,           # explicit structured param
        "time": parsed_time            # explicit structured param
    }

    response = agent_executor_with_history(user_input)

    output = response
    # print(output)
    # print(type(output))
    if isinstance(output, list) and len(output) > 0:
        answer_html = output[0].get("text", "")
    elif isinstance(output, str):
        answer_html = output
    else:
        answer_html = str(output)

    # print("answer :",answer_html)  
    # --- Save conversation history ---
    chat_history.append({
        "question": user_input,
        "answer": answer_html
    })
    save_chat(message_id, chat_history)

    frontend_payload = {
        "status_code": 200,
        "status": True,
        "message": "Message sent",
        "data": {
            "conversation": [
                {
                    "messageid": message_id,
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


# --- Local CLI Mode ---
if __name__ == "__main__":
    print("Welcome To Victoria's Public Transport Assistant")
    print("(Type 'exit' or 'quit' anytime to stop)\n")

    custom_message_id = input("Enter a message_id (or blank to auto-generate): ").strip()
    if not custom_message_id:
        custom_message_id = f"local-{datetime.now(timezone.utc).timestamp()}"

    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("Goodbye! Have a safe journey.")
            break

        event = {
            "body": json.dumps({
                "question": question,
                "messageid": custom_message_id
            })
        }

        response = lambda_handler(event, None)

        try:
            body = json.loads(response["body"])
            answer = body["data"]["conversation"][0]["answer"]
            print("\nAssistant:", answer, "\n")
        except Exception as e:
            print("Error parsing response:", e, "\n")
