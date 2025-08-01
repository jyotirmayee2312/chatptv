import requests


def get_train_departures(from_station: str, to_station: str) -> str:
    prompt_text = get_train_departures.format(input=input)
    url = f"http://52.63.39.167/api/find-trains?to={to_station.strip()}&from={from_station.strip()}"
    print(f"Calling URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        departures = data.get("departures", [])
        if not departures:
            return f"No departures found from {from_station} to {to_station}."
        next_dep = departures[0]
        return f"Next train from {data['from']} to {data['to']} departs at {next_dep['estimated_departure_utc']} from platform {next_dep.get('platform_number', 'N/A')}"
    else:
        return f"API error: {response.status_code}"