# train_assistant/main.py
# Run this script from the parent directory: python -m train_assistant.main

from train_assistant.agent.agent_executor import agent_executor

if __name__ == "__main__":
    print("Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("\nAsk something: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent_executor.invoke({"input": user_input})
        print("\n🧠 Agent Response:\n", response["output"])
