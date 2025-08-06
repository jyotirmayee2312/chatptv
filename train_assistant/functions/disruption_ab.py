# train_assistant/functions/disruption_ab.py

import requests

def check_disruptions_between_stations(from_station: str, to_station: str) -> str:
    try:
        train_resp = requests.get(
            f"http://52.63.39.167/api/find-trains?from={from_station}&to={to_station}"
        )
        train_resp.raise_for_status()
        train_data = train_resp.json()
        # print("train_data", train_data)

        departures = train_data.get("departures", [])
        # print("departures", departures)
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

        categorized = {
            "Major Disruptions": [],
            "Minor Delays": [],
            "Planned Works": []
        }

        for category in dis_data.get("disruptions", {}).values():
            for d in category:
                if d.get("disruption_id") in disruption_ids:
                    title_lower = d.get("title", "").lower()
                    if "major" in title_lower:
                        categorized["Major Disruptions"].append(d)
                    elif "delay" in title_lower:
                        categorized["Minor Delays"].append(d)
                    else:
                        categorized["Planned Works"].append(d)

        output = []
        for category, disruptions in categorized.items():
            if disruptions:
                output.append(f"**{category}**:")
                for d in disruptions:
                    output.append(f"- {d['title']}: {d['description'][:200]}...")
                output.append("")

        if not any(categorized.values()):
            return "Disruption IDs found but no matching details in current data."

        return "\n".join(output)

    except Exception as e:
        return f"Error checking disruptions: {e}"
