from langchain.tools import tool
from train_assistant.functions.disruption_line import check_disruptions_on_line
from train_assistant.functions.disruption_line import check_disruptions_on_line_vline
from pydantic import BaseModel, Field

# class TrainInput(BaseModel):
#     from_station: str
#     to_station: str


# @tool
# def check_disruptions_from_line(line_name: str) -> str:
#     try:
#         print("line_name", line_name)
#         return check_disruptions_on_line(line_name.strip())
#     except Exception as e:
#         return f"Error checking line disruption: {e}" 

# @tool
# def check_disruptions_from_line(input: str) -> str:
#     """
#     Tool: Check disruptions on a specific train line.
#     Input format: "route_type|line or route name"
#     route_type:
#       - 0 = Metro trains
#       - 3 = V/Line trains
#     """
#     try:
#         return check_disruptions_on_line(input.strip())
#     except Exception as e:
#         return f"Error checking line disruption: {e}"

@tool
def check_disruptions_from_line(input: str) -> str:
    """
    Tool: Check disruptions on a specific train line.

    Input format: "route_type|line or route name"
    route_type:
      - 0 = Metro trains
      - 3 = V/Line trains
    """
    try:
        # Split into route_type and line/route part
        route_type_str, line_name = input.split("|", 1)
        route_type = int(route_type_str.strip())
        line_name = line_name.strip()

        if route_type == 0:
            return check_disruptions_on_line(line_name)
        elif route_type == 3:
            return check_disruptions_on_line_vline(line_name)
        else:
            return f"Unsupported route_type: {route_type}"

    except Exception as e:
        return f"Error checking line disruption: {e}"
