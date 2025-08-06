# train_assistant/functions/find_train.py

import requests

def get_upcoming_trains(from_station: str, to_station: str) -> str:
    """
    Fetch upcoming train departures from API.
    """
    url = "http://52.63.39.167/api/find-trains"
    try:
        response = requests.get(url, params={"from": from_station, "to": to_station})
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Train API error: {e}"

    departures = data.get("departures", [])
    if not departures:
        return f"No departures found from {from_station} to {to_station}."

    # top_departures = departures[:3]
    results = []

    route_map = {
        1: "Alamein",
        2: "Belgrave",
        3: "Craigieburn",
        4: "Cranbourne",
        5: "Mernda",
        6: "Frankston",
        7: "Glen Waverley",
        8: "Hurstbridge",
        9: "Lilydale",
        11: "Pakenham",
        12: "Sandringham",
        13: "Stony Point",
        14: "Sunbury",
        15: "Upfield",
        16: "Werribee",
        17: "Williamstown",
        1482: "Flemington Racecourse",
    }

    for dep in departures[:3]:
        sched = dep.get("scheduled_departure_melbourne", "Unknown")
        est = dep.get("estimated_departure_melbourne")
        platform = dep.get("platform_number", "Unknown")
        run_id = dep.get("run_ref", "N/A")
        route_id = dep.get("route_id", -1)
        # route_name = route_map.get(route_id, "Unknown route")
        route_name = route_map.get(route_id, "Unknown line")

        line = f"Train {run_id} ({route_name}) at {sched}"
        print("line", line)
        if est and est != sched:
            line += f" (Est: {est})"
        line += f", Platform {platform}"
        results.append(line)

    return f"Upcoming trains from {from_station} to {to_station}:\n" + "\n".join(results)
    # print("top_departures", top_departures)
    # return top_departures
    # results = []
    # for dep in departures[:3]:  # Show next 3 departures
    #     sched = dep.get("scheduled_departure_utc", "Unknown")
    #     est = dep.get("estimated_departure_utc", "Unknown")
    #     platform = dep.get("platform_number", "Unknown")
    #     run_id = dep.get("run_ref", "N/A")

    #     line = f"Train {run_id} at {sched}"
    #     if est and est != sched:
    #         line += f" (Est: {est})"
    #     line += f", Platform {platform}"
    #     results.append(line)

    # return f"Upcoming trains from {from_station} to {to_station}:\n" + "\n".join(results)
