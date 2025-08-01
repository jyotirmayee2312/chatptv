import requests


def check_disruptions(line_name: str) -> str:
    url = f"http://52.63.39.167/api/check-disruptions?line={line_name.strip()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("disruptions"):
            return f"Disruptions on {line_name}: {data['disruptions']}"
        return f"No disruptions reported on {line_name}."
    return f"Failed to fetch disruption data."