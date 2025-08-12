# train_assistant/tools/timetable_tool.py
from typing import Optional
from langchain.tools import tool
from pydantic import BaseModel, Field
from train_assistant.functions.find_train import get_upcoming_trains
from train_assistant.context.conversation import context

class TrainInput(BaseModel):
    from_station: str = Field(..., description="Departure station")
    to_station: str = Field(..., description="Arrival station")
    date: Optional[str] = Field(None, description="Date of travel in YYYY-MM-DD format")
    time: Optional[str] = Field(None, description="Time of travel in HH:MM format (24-hour)")
@tool(args_schema=TrainInput)
# def train_tool(from_station: str, to_station: str) -> str:
def train_tool(from_station: str, to_station: str, date: Optional[str] = None, time: Optional[str] = None) -> str:
    """
    Tool: Get upcoming train departures between two stations. 
    Use ONLY when the query is about trains, train times, schedules, 
    routes, or departures between two stations.
    """
    # return get_upcoming_trains(from_station, to_station)
    return get_upcoming_trains(from_station, to_station, date, time)