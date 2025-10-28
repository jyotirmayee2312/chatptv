from typing import Optional
from langchain.tools import tool
from pydantic import BaseModel, Field
from functions.find_combined import get_upcoming_combined
from functions.datetime_parser import parse_natural_datetime, get_melbourne_date_string, get_melbourne_time_string


class CombinedTrainInput(BaseModel):
    query: Optional[str] = Field(
        None,
        description="Full user query including stations and date/time (optional if date/time are already provided)"
    )
    from_station: str = Field(..., description="Departure station")
    to_station: str = Field(..., description="Arrival station")
    date: Optional[str] = Field(
        None,
        description="Date of travel in YYYY-MM-DD format (e.g., '2025-09-06'). If not provided, will be parsed from query or default to today."
    )
    time: Optional[str] = Field(
        None,
        description="Time of travel in HH:MM AM/PM format (e.g., '10:00 PM'). If not provided, will be parsed from query or default to now."
    )


@tool(args_schema=CombinedTrainInput)
def combined_timetable_tool(
    query: Optional[str] = None,
    from_station: str = None,
    to_station: str = None,
    date: Optional[str] = None,
    time: Optional[str] = None
) -> str:
    """
    Tool: Get upcoming departures for BOTH Train and V/Line between two stations.
    - If date/time provided explicitly, they take priority.
    - Otherwise, parse from query.
    - If nothing is found, defaults to current Melbourne date/time.
    """
    # Only parse from query if date/time not explicitly provided
    if not date or not time:
        parsed_date, parsed_time = parse_natural_datetime(query or "")
        date = date or parsed_date
        time = time or parsed_time

    # Final fallback → current Melbourne datetime
    if not date:
        date = get_melbourne_date_string()
    if not time:
        time = get_melbourne_time_string()

    print(f"[combined_timetable_tool] Using from={from_station}, to={to_station}, date={date}, time={time}")

    return get_upcoming_combined(from_station, to_station, date, time)
