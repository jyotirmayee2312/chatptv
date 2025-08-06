import requests

# def check_disruptions_on_line(line_name: str) -> str:
#     try:
#         resp = requests.get(f"http://52.63.39.167/api/disruption-line?line={line_name}")
#         resp.raise_for_status()
#         data = resp.json()

#         if not data.get("disruptions"):
#             return f"No current disruptions reported on the {line_name}."
        
#         disruptions = "\n".join(data["disruptions"])
#         return f"Disruptions on {line_name}:\n{disruptions}"
#     except Exception as e:
#         return f"Failed to fetch disruptions for {line_name}: {e}"
    

# train_assistant/functions/disruption_line.py

import requests

def check_disruptions_on_line(line_name: str) -> str:
    """
    Check disruptions on a specific train line by matching route names.
    Example: 'Belgrave', 'Sunbury', 'Werribee'
    """
    try:
        dis_resp = requests.get("http://52.63.39.167/api/ptv/disruptions")
        dis_resp.raise_for_status()
        dis_data = dis_resp.json()

        line_name = line_name.strip().lower()
        print("line_name", line_name)
        categorized = {
            "Major Disruptions": [],
            "Minor Delays": [],
            "Planned Works": []
        }

        found = False
        for category in dis_data.get("disruptions", {}).values():
            print("dis data",dis_data)

            for d in category:
                for route in d.get("routes", []):
                    route_name = route.get("route_name", "").lower()
                    if line_name in route_name:
                        found = True
                        title_lower = d.get("title", "").lower()
                        if "major" in title_lower:
                            categorized["Major Disruptions"].append(d)
                        elif "delay" in title_lower:
                            categorized["Minor Delays"].append(d)
                        else:
                            categorized["Planned Works"].append(d)
                        break  # only match one route per disruption

        if not found:
            return f"No disruptions found for the '{line_name}' line."

        output = []
        for category, disruptions in categorized.items():
            if disruptions:
                output.append(f"**{category}**:")
                for d in disruptions:
                    output.append(f"- {d['title']}: {d['description'][:200]}...")
                output.append("")

        return "\n".join(output)

    except Exception as e:
        return f"Error checking line disruptions: {e}"

