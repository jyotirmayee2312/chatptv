# train_assistant/tools/disruption_tool.py

# from langchain.tools import tool
# from train_assistant.functions.disruption_ab import check_disruptions_between_stations

# @tool
# def check_disruptions_from_route(input: str) -> str:
#     """
#     Tool: Check disruptions between two stations.
#     Input format: "StationA to StationB"
#     """
#     try:
#         from_station, to_station = input.split(" to ")
#         return check_disruptions_between_stations(from_station.strip(), to_station.strip())
#     except Exception as e:
#         return f"Error parsing input: {e}"

from langchain.tools import tool
from train_assistant.functions.disruption_ab import check_disruptions_between_stations
from train_assistant.context.conversation import context

@tool
def check_disruptions_from_route(input: str) -> str:
    """
    Tool: Check disruptions between two stations.
    Input format: "StationA to StationB"
    """
    try:
        # Direct input format: "StationA to StationB"
        if " to " in input:
            from_station, to_station = input.split(" to ")
            # Save this route to context
            context.update_last_route(f"{from_station.strip()} to {to_station.strip()}")
        else:
            # Fallback to memory if route not provided
            last_route = context.get_last_route()
            if not last_route:
                return "No route provided and no recent route found in memory."
            from_station, to_station = last_route

        return check_disruptions_between_stations(from_station.strip(), to_station.strip())
    except Exception as e:
        return f"Error parsing input or accessing route: {e}"


# @tool
# def check_disruptions_from_route(input: str) -> str:
#     """
#     Tool: Check disruptions for a given route or line.
#     Input format:
#     - "StationA to StationB"
#     - "Upfield" or "Belgrave line" or station name
#     """
#     try:
#         return check_disruptions_between_stations(input.strip())
#     except Exception as e:
#         return f"Error checking disruptions: {e}"
