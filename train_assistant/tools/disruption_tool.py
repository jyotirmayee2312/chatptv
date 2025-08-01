# train_assistant/tools/disruption_tool.py

from langchain.tools import tool
from train_assistant.functions.disruption_ab import check_disruptions_between_stations

@tool
def check_disruptions_from_route(input: str) -> str:
    """
    Tool: Check disruptions between two stations.
    Input format: "StationA to StationB"
    """
    try:
        from_station, to_station = input.split(" to ")
        return check_disruptions_between_stations(from_station.strip(), to_station.strip())
    except Exception as e:
        return f"Error parsing input: {e}"
