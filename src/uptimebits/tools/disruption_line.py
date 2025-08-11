from langchain.tools import tool
from functions.disruption_line import check_disruptions_on_line
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


@tool
def check_disruptions_from_line(input: str) -> str:
    """
    Tool: Check disruptions on a specific train line.
    Input format: Name of the train line (e.g., "Belgrave line").
    """
    try:
        return check_disruptions_on_line(input.strip())
    except Exception as e:
        return f"Error checking line disruption: {e}"
