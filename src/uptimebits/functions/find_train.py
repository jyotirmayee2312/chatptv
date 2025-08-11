# train_assistant/functions/find_train.py

import requests
# train_assistant/functions/find_train.py

from context.conversation import context

# def get_upcoming_trains(from_station: str, to_station: str) -> str:
def get_upcoming_trains(from_station: str, to_station: str, date: str = None, time: str = None) -> str:
    """
    Fetch upcoming train departures from API.
    """
    url = "http://52.63.39.167/api/find-trains"
    params= {}
    if date:
        params["date"] = date  # e.g. 2025-08-09
    if time:
        params["time"] = time  # e.g. 18:00


    try:
        response = requests.get(url, params={"from": from_station, "to": to_station})
        context.update_last_route(f"{from_station.strip()} to {to_station.strip()}")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Train API error: {e}"

    departures = data.get("departures", [])
    if not departures:
        return f"No departures found from {from_station} to {to_station}."

    results = []
    for dep in departures[:3]:  # Show next 3 departures
        sched = dep.get("scheduled_departure_utc", "Unknown")
        est = dep.get("estimated_departure_utc", "Unknown")
        platform = dep.get("platform_number", "Unknown")
        run_id = dep.get("run_ref", "N/A")
        route_name = dep.get("route_name", "Unknown")
        # journey_time = dep.get("journey_time_minutes", "Unknown")

        line = f"[{route_name} Line] Train {run_id} at {sched}"
        if est and est != sched:
            line += f" (Est: {est})"
        line += f", Platform {platform}"
        results.append(line)

    return f"Upcoming trains from {from_station} to {to_station}:\n" + "\n".join(results)