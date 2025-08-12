# train_assistant/tools/disruption_tool.py

# from langchain.tools import tool
# from train_assistant.functions.disruption_ab import check_disruptions_between_stations
# from train_assistant.context.conversation import context
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

# train_assistant/tools/disruption_tool.py

from langchain.tools import tool
from train_assistant.functions.disruption_ab import (
    check_disruptions_between_stations,
    check_disruptions_between_stations_vline
)

# train_assistant/tools/disruption_tool.py

from langchain.tools import tool
from pydantic import BaseModel
from train_assistant.functions.disruption_ab import (
    check_disruptions_between_stations,
    check_disruptions_between_stations_vline
)

class RouteDisruptionInput(BaseModel):
    route_type: int  # 0 = Metro, 3 = V/Line
    from_station: str
    to_station: str

@tool(args_schema=RouteDisruptionInput)
def check_disruptions_from_route(route_type: int, from_station: str, to_station: str) -> str:
    """
    Tool: Check disruptions between two stations.
    route_type:
      - 0 = Metro trains
      - 3 = V/Line trains
    """
    try:
        if route_type == 0:
            return check_disruptions_between_stations(from_station.strip(), to_station.strip())
        elif route_type == 3:
            return check_disruptions_between_stations_vline(from_station.strip(), to_station.strip())
        else:
            return f"Unsupported route_type: {route_type}"
    except Exception as e:
        return f"Error checking disruptions: {e}"
