# train_assistant/functions/find_vline.py

import requests
from context.conversation import context


def get_upcoming_vline(from_station: str, to_station: str, date: str , time: str) -> str:
    """
    Fetch upcoming V/Line (route_type=3) departures from API.
    API expects:
    - date: YYYY-MM-DD format (e.g., "2025-09-06")
    - time: HH:MM AM/PM format (e.g., "10:00 PM")
    """
    url = "http://52.63.39.167/api/find-trains"
    params = {
        "from": from_station,
        "to": to_station,
        "route_type": 3  # V/Line / regional
    }

    # Add date/time params if provided
    if date:
        params["date"] = date  # e.g., "2025-09-06"
    if time:
        params["time"] = time  # e.g., "10:00 PM"

    try:
        response = requests.get(url, params=params)
        context.update_last_route(f"{from_station.strip()} to {to_station.strip()} (V/Line)")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"V/Line API error: {e}"

    departures = data.get("shortest_journey", [])
    if not departures:
        return f"No V/Line departures found from {from_station} to {to_station}."

    results = []
    for dep in departures[:3]:  # Show next 3 departures
        sched = dep.get("scheduled_departure_melbourne", "Unknown")
        est = dep.get("estimated_departure_melbourne", None)
        platform = dep.get("platform_number", "Unknown")
        run_id = dep.get("run_ref", "N/A")
        route_name = dep.get("route_name", "Unknown")
        stop_name = dep.get("stop_name", "")
        journey_time = dep.get("journey_time_minutes", "Unknown")

        line = f"V/Line {route_name} (Run {run_id}) departs {stop_name} at {sched}"
        if est and est != sched:
            line += f" (Est: {est})"
        if platform:
            line += f", Platform {platform}"
        if journey_time is not None:
            line += f", Journey time: {journey_time} mins"
        results.append(line)

    # Add date/time context to response if provided
    context_info = ""
    if date and time:
        context_info = f" for {date} at {time}"
    elif date:
        context_info = f" for {date}"
    elif time:
        context_info = f" at {time}"

    return f"<b>V/Line Services from {from_station} to {to_station}{context_info}:</b><br>" + "<br>".join(f" {result}" for result in results)
    # return f"Upcoming V/Line departures from {from_station} to {to_station}:\n" + "\n".join(results)