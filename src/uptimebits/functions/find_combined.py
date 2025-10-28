# train_assistant/functions/find_combined.py

from functions.find_train import get_upcoming_trains
from functions.find_vline import get_upcoming_vline

def get_upcoming_combined(from_station: str, to_station: str, date: str , time: str ) -> dict:
    """
    Fetch both Train (route_type=0) and V/Line (route_type=3) departures
    and return combined results as a formatted string.
    API expects:
    - date: YYYY-MM-DD format (e.g., "2025-09-06")
    - time: HH:MM AM/PM format (e.g., "10:00 PM")
    """
    print("date:",date)
    print("time:",time)
    train_result = get_upcoming_trains(from_station, to_station, date, time)
    vline_result = get_upcoming_vline(from_station, to_station, date, time)

    # Add date/time context to response if provided
    context_info = ""
    if date and time:
        context_info = f" for {date} at {time}"
    elif date:
        context_info = f" for {date}"
    elif time:
        context_info = f" at {time}"
        
    # result = {
    #     "from_station": from_station,
    #     "to_station": to_station,
    #     "date": date,
    #     "time": time,
    #     "train": None,
    #     "vline": None
    # }
    # Format combined results
    combined_result = f"<b>Combined Train & V/Line Options from {from_station} to {to_station}{context_info}:</b><br><br>"

    if "No metro train departures found" not in train_result:
        combined_result += train_result + "<br><br>"
    else:
        combined_result += f"<b> Metro Trains:</b><br>No metro train services found<br><br>"

    # Add V/Line results  
    if "No V/Line departures found" not in vline_result:
        combined_result += vline_result + "<br><br>"
    else:
        combined_result += f"<b>V/Line Services:</b><br>No V/Line services found<br><br>"


    return combined_result
