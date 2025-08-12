# train_assistant/functions/find_vline.py

import requests
from train_assistant.context.conversation import context


def get_upcoming_vline(from_station: str, to_station: str, date: str = None, time: str = None) -> str:
    """
    Fetch upcoming V/Line (route_type=3) departures from API.
    """
    url = "http://52.63.39.167/api/find-trains"
    params = {
        "from": from_station,
        "to": to_station,
        "route_type": 3  # V/Line / regional
    }
    if date:
        params["date"] = date
    if time:
        params["time"] = time

    try:
        response = requests.get(url, params=params)
        context.update_last_route(f"{from_station.strip()} to {to_station.strip()} (V/Line)")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"V/Line API error: {e}"

    departures = data.get("departures", [])
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

        line = f"V/Line {route_name} (Run {run_id}) departs {stop_name} at {sched}"
        if est and est != sched:
            line += f" (Est: {est})"
        if platform:
            line += f", Platform {platform}"
        results.append(line)

    return f"Upcoming V/Line departures from {from_station} to {to_station}:\n" + "\n".join(results)
