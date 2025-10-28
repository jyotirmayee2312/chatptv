# train_assistant/functions/disruption_ab.py

import requests
from collections import defaultdict

def check_disruptions_between_stations(from_station: str, to_station: str) -> str:
    """
    Checks Metro train disruptions (route_type=0).
    """
    return _check_disruptions(from_station, to_station, route_type=0)

def check_disruptions_between_stations_vline(from_station: str, to_station: str) -> str:
    """
    Checks V/Line disruptions (route_type=3).
    """
    return _check_disruptions(from_station, to_station, route_type=3)

def _check_disruptions(from_station: str, to_station: str, route_type: int) -> str:
    try:
        # Fetch departures
        train_resp = requests.get(
            f"http://52.63.39.167/api/find-trains?from={from_station}&to={to_station}&route_type={route_type}"
        )
        train_resp.raise_for_status()
        train_data = train_resp.json()

        departures = train_data.get("departures", [])
        if not departures:
            return f"No departures found from {from_station} to {to_station} (route_type={route_type})."

        # Collect disruption IDs
        disruption_ids = set()
        for dep in departures:
            disruption_ids.update(dep.get("disruption_ids", []))

        if not disruption_ids:
            return f"No disruptions reported between {from_station} and {to_station} (route_type={route_type})."

        # Fetch disruption details for the given route_type
        dis_resp = requests.get(f"http://52.63.39.167/api/ptv/disruptions?route_type={route_type}")
        dis_resp.raise_for_status()
        dis_data = dis_resp.json()

        categorized = defaultdict(list)  # disruption_type -> [disruption]

        for category_list in dis_data.get("disruptions", {}).values():
            for disruption in category_list:
                if disruption.get("disruption_id") in disruption_ids:
                    dtype = disruption.get("disruption_type", "Unknown")
                    categorized[dtype].append(disruption)

        if not categorized:
            return "Disruption IDs found but no matching details in current data."

        # Format the output
        output = [f"Disruptions between **{from_station}** and **{to_station}** (route_type={route_type}):\n"]
        for dtype, items in categorized.items():
            output.append(f"**{dtype}**:")
            for d in items:
                title = d.get("title", "No title")
                desc = d.get("description", "")[:200] + "..."
                output.append(f"- {title}: {desc}")
            output.append("")  # spacing

        return "\n".join(output)

    except Exception as e:
        return f"Error checking disruptions: {e}"
