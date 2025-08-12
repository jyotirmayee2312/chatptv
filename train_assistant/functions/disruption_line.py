# # train_assistant/functions/disruption_line.py

# import requests
# import difflib

# def check_disruptions_on_line(line_name: str) -> str:
#     try:
#         dis_resp = requests.get("http://52.63.39.167/api/ptv/disruptions")
#         dis_resp.raise_for_status()
#         dis_data = dis_resp.json()

#         user_input = line_name.lower().replace(" line", "").strip()
        
#         # Collect all route names
#         all_routes = {}
#         for category in dis_data.get("disruptions", {}).values():
#             for d in category:
#                 for route in d.get("routes", []):
#                     route_name = route.get("route_name", "").strip()
#                     all_routes[route_name.lower()] = route_name

#         # Find best match
#         best_match = difflib.get_close_matches(user_input, all_routes.keys(), n=1, cutoff=0.6)
#         if not best_match:
#             return f"No matching line found for '{line_name}'"

#         matched_line = all_routes[best_match[0]]
#         disruptions = []
        
#         for category in dis_data.get("disruptions", {}).values():
#             for d in category:
#                 if any(route.get("route_name", "").strip() == matched_line 
#                    for route in d.get("routes", [])):
#                     desc = d.get("description", "No details available")
#                     disruptions.append(f"- {d.get('title')}: {desc[:200]}{'...' if len(desc) > 200 else ''}")

#         if not disruptions:
#             return f"No current disruptions on {matched_line} line"
            
#         return f"Disruptions on {matched_line} line:\n" + "\n".join(disruptions)

#     except Exception as e:
#         return f"Error checking disruptions: {str(e)}"

# train_assistant/functions/disruption_line.py

import requests
import difflib

def _check_disruptions_on_line(line_name: str, route_type: int) -> str:
    """
    Internal helper to check disruptions for a given line and route_type.
    route_type:
      - 0 = Metro trains
      - 3 = V/Line trains
    """
    try:
        # Pass route_type to backend
        dis_resp = requests.get(f"http://52.63.39.167/api/ptv/disruptions?route_type={route_type}")
        dis_resp.raise_for_status()
        dis_data = dis_resp.json()

        user_input = line_name.lower().replace(" line", "").strip()

        # Collect all route names
        all_routes = {}
        for category in dis_data.get("disruptions", {}).values():
            for d in category:
                for route in d.get("routes", []):
                    route_name = route.get("route_name", "").strip()
                    if route_name:
                        all_routes[route_name.lower()] = route_name

        # Find best match
        best_match = difflib.get_close_matches(user_input, all_routes.keys(), n=1, cutoff=0.6)
        if not best_match:
            return f"No matching line found for '{line_name}'"

        matched_line = all_routes[best_match[0]]
        disruptions = []

        for category in dis_data.get("disruptions", {}).values():
            for d in category:
                if any(route.get("route_name", "").strip() == matched_line
                       for route in d.get("routes", [])):
                    desc = d.get("description", "No details available")
                    disruptions.append(
                        f"- {d.get('title')}: {desc[:200]}{'...' if len(desc) > 200 else ''}"
                    )

        if not disruptions:
            return f"No current disruptions on {matched_line} line"

        return f"Disruptions on {matched_line} line:\n" + "\n".join(disruptions)

    except Exception as e:
        return f"Error checking disruptions: {str(e)}"


def check_disruptions_on_line(line_name: str) -> str:
    """
    Metro train disruptions (route_type=0)
    """
    return _check_disruptions_on_line(line_name, route_type=0)


def check_disruptions_on_line_vline(line_name: str) -> str:
    """
    V/Line train disruptions (route_type=3)
    """
    return _check_disruptions_on_line(line_name, route_type=3)
