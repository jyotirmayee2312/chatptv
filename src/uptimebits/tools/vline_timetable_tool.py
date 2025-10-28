# train_assistant/tools/vline_timetable_tool.py
from typing import Optional
from langchain.tools import tool
from pydantic import BaseModel, Field
from functions.find_vline import get_upcoming_vline
from functions.datetime_parser import parse_natural_datetime

class VlineTrainInput(BaseModel):
    query: str = Field(..., description="Full user query including stations and date/time")
    from_station: str = Field(..., description="Departure station")
    to_station: str = Field(..., description="Arrival station")
    date: Optional[str] = Field(None, description="Date of travel in YYYY-MM-DD format (e.g., '2025-09-06')")
    time: Optional[str] = Field(None, description="Time of travel in HH:MM AM/PM format (e.g., '10:00 PM')")

@tool(args_schema=VlineTrainInput)
def vline_train_tool(query: str, from_station: str, to_station: str, date: Optional[str] = None, time: Optional[str] = None) -> str:
    """
    Tool: Get upcoming V/Line departures (route_type=3) between two stations. 
    Automatically parses date/time from the query if not provided.
    Include date and time if provided.
    """
    # Parse date/time from query if not explicitly provided
    parsed_date, parsed_time = None, None
    print("Parsed date & time:",parsed_date,parsed_time)
    # if not date or not time:
    #     parsed_date, parsed_time = parse_natural_datetime(query)
    #     date = date or parsed_date
    #     time = time or parsed_time
    parsed_date, parsed_time = parse_natural_datetime(query)
    print(f"vline_tool: Using date={parsed_date}, time={parsed_time}")  # Debug log
    return get_upcoming_vline(from_station, to_station, parsed_date, parsed_time)