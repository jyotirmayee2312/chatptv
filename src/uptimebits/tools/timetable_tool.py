
# train_assistant/tools/timetable_tool.py
from typing import Optional
# from langchain.tools import tool
from pydantic import BaseModel, Field
from functions.find_train import get_upcoming_trains
from functions.datetime_parser import parse_natural_datetime
from strands import tool, Agent

class TrainInput(BaseModel):
    query: str = Field(..., description="Full user query including stations and date/time")
    from_station: str = Field(..., description="Departure station")
    to_station: str = Field(..., description="Arrival station") 
    date: Optional[str] = Field(None, description="Date of travel in YYYY-MM-DD format (e.g., '2025-09-06')")
    time: Optional[str] = Field(None, description="Time of travel in HH:MM AM/PM format (e.g., '10:00 PM')")

@tool
def train_tool(query: str, from_station: str, to_station: str, date: Optional[str] = None, time: Optional[str] = None) -> str:
    """
    Tool: Get upcoming train departures between two stations. 
    Automatically parses date/time from the query if not provided.
    Use ONLY when the query is about trains, train times, schedules, 
    routes, or departures between two stations.
    """
    # Parse date/time from query if not explicitly provided
    parsed_date, parsed_time = None, None
    print("Parsed date & time:",parsed_date,parsed_time)
    # if not date or not time:
    #     parsed_date, parsed_time = parse_natural_datetime(query)
    #     date = date or parsed_date
    #     time = time or parsed_time
    parsed_date, parsed_time = parse_natural_datetime(query)
    print(f"train_tool: Using date={date}, time={time}")  # Debug log
    return get_upcoming_trains(from_station, to_station, parsed_date, parsed_time)