# train_assistant/tools/disruption_tool.py

from langchain.tools import tool
from functions.disruption_ab import check_disruptions_between_stations
from pydantic import BaseModel



class TrainInput(BaseModel):
    from_station: str
    to_station: str

@tool(args_schema=TrainInput)
def check_disruptions_from_route(from_station: str, to_station: str) -> str:
    """
    Tool: Check disruptions between two stations.
    Input format: "StationA to StationB"
    """
    try:
        # from_station, to_station = input.split(" to ")
        print("from_station", from_station)
        print("to_station", to_station)
        return check_disruptions_between_stations(from_station.strip(), to_station.strip())
    except Exception as e:
        return f"Error parsing input: {e}"
    


# train_assistant/tools/disruption_tool.py

# from langchain.tools import tool
# from functions.disruption_ab import check_disruptions_between_stations
# from context.conversation import context
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
