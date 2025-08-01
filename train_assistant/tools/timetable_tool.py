# train_assistant/tools/timetable_tool.py

from langchain.tools import tool
from pydantic import BaseModel, Field
from train_assistant.functions.find_train import get_upcoming_trains

class TrainInput(BaseModel):
    from_station: str = Field(..., description="Departure station")
    to_station: str = Field(..., description="Arrival station")

@tool(args_schema=TrainInput)
def train_tool(from_station: str, to_station: str) -> str:
    """
    Tool: Get upcoming train departures between two stations.
    """
    return get_upcoming_trains(from_station, to_station)
