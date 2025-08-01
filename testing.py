from pydantic import BaseModel
from langchain_aws import ChatBedrock
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import requests

# --- LLM Setup ---
llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1",
)

# --- Tool Schemas ---
class TrainInput(BaseModel):
    from_station: str
    to_station: str

# --- Train tool ---
@tool(args_schema=TrainInput)
def train_tool(from_station: str, to_station: str) -> str:
    """
    Get upcoming train departures from `from_station` to `to_station`.
    """
    url = "http://52.63.39.167/api/find-trains"
    try:
        response = requests.get(url, params={"from": from_station, "to": to_station})
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Train API error: {e}"

    # Format the train data for display
    departures = data.get("departures", [])
    if not departures:
        return f"No departures found from {from_station} to {to_station}."

    results = []
    for dep in departures[:3]:  # Show next 3 departures
        sched = dep.get("scheduled_departure_utc", "Unknown")
        est = dep.get("estimated_departure_utc", "Unknown")
        platform = dep.get("platform_number", "Unknown")
        run_id = dep.get("run_ref", "N/A")

        line = f"Train {run_id} at {sched}"
        if est and est != sched:
            line += f" (Est: {est})"
        line += f", Platform {platform}"
        results.append(line)

    return f"Upcoming trains from {from_station} to {to_station}:\n" + "\n".join(results)


# --- Disruptions tool ---
@tool
def check_disruptions_from_route(input: str) -> str:
    """
    Check disruptions between two stations.
    Input format: "StationA to StationB".
    """
    try:
        from_station, to_station = input.split(" to ")
        from_station = from_station.strip()
        to_station = to_station.strip()

        train_resp = requests.get(
            f"http://52.63.39.167/api/find-trains?from={from_station}&to={to_station}"
        )
        train_resp.raise_for_status()
        train_data = train_resp.json()

        departures = train_data.get("departures", [])
        if not departures:
            return f"No departures found from {from_station} to {to_station}."

        disruption_ids = set()
        for dep in departures:
            disruption_ids.update(dep.get("disruption_ids", []))

        if not disruption_ids:
            return f"No disruptions reported between {from_station} and {to_station}."

        dis_resp = requests.get("http://52.63.39.167/api/ptv/disruptions")
        dis_resp.raise_for_status()
        dis_data = dis_resp.json()

        categorized = {
            "Major Disruptions": [],
            "Minor Delays": [],
            "Planned Works": []
        }

        for category in dis_data.get("disruptions", {}).values():
            for d in category:
                if d.get("disruption_id") in disruption_ids:
                    title_lower = d.get("title", "").lower()
                    if "major" in title_lower:
                        categorized["Major Disruptions"].append(d)
                    elif "delay" in title_lower:
                        categorized["Minor Delays"].append(d)
                    else:
                        categorized["Planned Works"].append(d)

        output = []
        for category, disruptions in categorized.items():
            if disruptions:
                output.append(f"**{category}**:")
                for d in disruptions:
                    output.append(f"- {d['title']}: {d['description'][:200]}...")
                output.append("")

        if not any(categorized.values()):
            return "Disruption IDs found but no matching details in current data."

        return "\n".join(output)

    except Exception as e:
        return f"Error checking disruptions: {e}"

# --- Irrelevant query handler ---
@tool
def handle_irrelevant_query(input: str) -> str:
    """
    Respond to queries unrelated to Melbourne train services.
    """
    return ("I specialize in Melbourne train services only. "
            "Please ask about train schedules or disruptions.")

# --- Tools list ---
tools = [train_tool, check_disruptions_from_route, handle_irrelevant_query]

# --- Router prompt ---
router_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a router assistant that chooses the best tool to answer questions about Melbourne trains."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

router_agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=router_prompt)
executor = AgentExecutor(agent=router_agent, tools=tools, verbose=True)

if __name__ == "__main__":
    print("Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("\nAsk something: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = executor.invoke({"input": user_input})
        print("\n🧠 Agent Response:\n", response["output"])
