# train_assistant/functions/find_combined.py

from train_assistant.functions.find_train import get_upcoming_trains
from train_assistant.functions.find_vline import get_upcoming_vline

def get_upcoming_combined(from_station: str, to_station: str, date: str = None, time: str = None) -> dict:
    """
    Fetch both Train (route_type=0) and V/Line (route_type=3) departures
    and return structured results as a dictionary.
    """
    train_result = get_upcoming_trains(from_station, to_station, date, time)
    vline_result = get_upcoming_vline(from_station, to_station, date, time)

    result = {
        "from_station": from_station,
        "to_station": to_station,
        "date": date,
        "time": time,
        "train": None,
        "vline": None
    }

    # Train
    if "No departures found" not in train_result:
        result["train"] = train_result
    else:
        result["train"] = []

    # V/Line
    if "No V/Line departures found" not in vline_result:
        result["vline"] = vline_result
    else:
        result["vline"] = []

    return result
