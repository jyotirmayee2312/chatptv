# train_assistant/main.py
# Run this script from the parent directory: python -m train_assistant.main

from train_assistant.agent.agent_executor import agent_executor
from train_assistant.context.conversation import context

if __name__ == "__main__":
    print("Welcome To the Victoria's Public Transport Assistant!")
    print("(Type 'exit' or 'quit' anytime to stop.)\n")

    while True:
        user_input = input("What would you like to know?\n>")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Have a safe journey.")
            break
        if not user_input:
            print("You haven't entered anything. Ask me something about your train journey!")
            continue

        context.add_message("User", user_input)

        response = agent_executor.invoke({
            "input": user_input,
            "chat_history":context.get_history()
        })
        print("\nResponse:")
        output = response.get("output")
        if isinstance(output, list):
            for item in output:
                if item.get("type") == "text":
                    print(item.get("text"))
        else:
            print(output)