# train_assistant/functions/disruption_ab.py


import requests
from collections import defaultdict

def check_disruptions_between_stations(from_station: str, to_station: str) -> str:
    try:
        train_resp = requests.get(
            f"http://52.63.39.167/api/find-trains?from={from_station}&to={to_station}"
        )
        train_resp.raise_for_status()
        train_data = train_resp.json()

        departures = train_data.get("departures", [])
        if not departures:
            return f"No departures found from {from_station} to {to_station}."

        disruption_ids = set()
        for dep in departures:
            disruption_ids.update(dep.get("disruption_ids", []))

        if not disruption_ids:
            return f"No disruptions reported between {from_station} and {to_station}."

        dis_resp = requests.get("http://52.63.39.167/api/ptv/disruptions")
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

        # Step 4: Format the output nicely
        output = [f"Disruptions between **{from_station}** and **{to_station}**:\n"]
        for dtype, items in categorized.items():
            output.append(f"**{dtype}**:")
            for d in items:
                title = d.get("title", "No title")
                desc = d.get("description", "")[:200] + "..."
                output.append(f"- {title}: {desc}")
            output.append("")  # Add spacing between sections

        return "\n".join(output)

    except Exception as e:
        return f"Error checking disruptions: {e}"