# train_assistant/tools/vline_timetable_tool.py

from typing import Optional
from langchain.tools import tool
from pydantic import BaseModel, Field
from train_assistant.functions.find_vline import get_upcoming_vline
from train_assistant.context.conversation import context

class VlineTrainInput(BaseModel):
    from_station: str = Field(..., description="Departure station")
    to_station: str = Field(..., description="Arrival station")
    date: Optional[str] = Field(None, description="Date of travel in YYYY-MM-DD format")
    time: Optional[str] = Field(None, description="Time of travel in HH:MM format (24-hour)")

@tool(args_schema=VlineTrainInput)
def vline_train_tool(from_station: str, to_station: str, date: Optional[str] = None, time: Optional[str] = None) -> str:
    """
    Tool: Get upcoming V/Line departures (route_type=3) between two stations. 
    Include date and time if provided.
    """
    return get_upcoming_vline(from_station, to_station, date, time)
