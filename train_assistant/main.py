# train_assistant/main.py
# Run this script from the parent directory: python -m train_assistant.main

from train_assistant.agent.agent_executor import agent_executor
from train_assistant.context.conversation import context

if __name__ == "__main__":
    print("Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("\nAsk something: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent_executor.invoke({
            "input": user_input,
            "chat_history":context.get_history()
        })
        print("\nResponse:\n", response["output"], "\n")
        print("\n🧠 Agent Response:\n", response["output"])


# if __name__ == "__main__":
#     print("Welcome to the Victoria Public Transport Assistant!\n")
#     while True:
#         user_input = input("What would you like to know?\n>")

#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye! Have a safe journey.")
#             break

#         if not user_input:
#             print("You haven’t entered anything. Ask me something about your train journey!")
#             continue

#         try:
#             response = agent_executor.invoke({
#                 "input": user_input,
#                 "chat_history":context.get_history()
#             })
#             final_answer = response.get("output")
#             print("\nResponse:\n", final_answer,  "\n")
#         except Exception as e:
#             print("Something went wrong while processing your request.")
#             print("Error:", e)