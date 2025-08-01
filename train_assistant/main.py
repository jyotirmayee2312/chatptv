from agents.route_agent import run_route_agent

def main():
    print("Train Assistant is running...")
    while True:
        user_input = input("How can I help you? ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = run_route_agent(user_input)
        print(response)

if __name__ == "__main__":
    main()