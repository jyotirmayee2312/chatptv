import boto3
import requests
import difflib
import json
import importlib.resources as pkg_resources
import os
# # Load route_reference.json
# with pkg_resources.files("context").joinpath("route_reference.json").open("r", encoding="utf-8") as f:
#     ROUTE_DATA = json.load(f)

# Load route_reference.json from S3
s3 = boto3.client("s3")
bucket = os.environ.get("CHAT_HISTORY_BUCKET", "chathistorybucket-chatbuddy")
key = "route_reference/route_reference.json"

obj = s3.get_object(Bucket=bucket, Key=key)
ROUTE_DATA = json.loads(obj["Body"].read().decode("utf-8"))


def _normalize_name(name: str) -> str:
    """Normalize names for comparison (lowercased, stripped)."""
    return name.strip().lower()


def _find_best_line_match(line_name: str, valid_lines: list[str]) -> str | None:
    """
    Find the closest line name match:
    1. Exact/substring match (case-insensitive).
    2. If multiple substring matches, return a "Multiple matches" message.
    3. Fallback to fuzzy matching via difflib.
    """
    line_name_norm = _normalize_name(line_name)

    # --- Step 1: Substring search ---
    substring_matches = [
        line for line in valid_lines if line_name_norm in _normalize_name(line)
    ]
    if len(substring_matches) == 1:
        return substring_matches[0]
    elif len(substring_matches) > 1:
        return f"Multiple matches: {', '.join(substring_matches)}"

    # --- Step 2: Fuzzy match ---
    valid_names_norm = [_normalize_name(line) for line in valid_lines]
    match = difflib.get_close_matches(line_name_norm, valid_names_norm, n=1, cutoff=0.6)
    if match:
        idx = valid_names_norm.index(match[0])
        return valid_lines[idx]

    return None


def _search_across_types(line_name: str) -> tuple[str | None, int | None]:
    """Try finding the line across both Metro and V/Line routes."""
    for system in ["metro", "vline"]:
        valid_lines = ROUTE_DATA[system]["lines"]
        matched_line = _find_best_line_match(line_name, valid_lines)
        if matched_line:
            return matched_line, ROUTE_DATA[system]["route_type"]
    return None, None


def _check_disruptions_on_line(line_name: str, route_type: int) -> str:
    """
    Check disruptions for a given line (metro or V/Line) using backend API.
    """
    try:
        # Resolve the line name via ROUTE_DATA
        valid_lines = []
        if route_type == ROUTE_DATA["metro"]["route_type"]:
            valid_lines = ROUTE_DATA["metro"]["lines"]
        elif route_type == ROUTE_DATA["vline"]["route_type"]:
            valid_lines = ROUTE_DATA["vline"]["lines"]

        matched_line = _find_best_line_match(line_name, valid_lines) if valid_lines else None

        # If not found in current type, search across both types
        if not matched_line or matched_line.startswith("Multiple"):
            matched_line, route_type = _search_across_types(line_name)

        if not matched_line:
            return f"No line found for '{line_name}' in metro or V/Line routes."

        # ---- Backend API Call ----
        dis_resp = requests.get(f"http://52.63.39.167/api/ptv/disruptions?route_type={route_type}")
        dis_resp.raise_for_status()
        dis_data = dis_resp.json()

        disruptions = []
        for category in dis_data.get("disruptions", {}).values():
            for d in category:
                if any(
                    _normalize_name(route.get("route_name", "")) == _normalize_name(matched_line)
                    for route in d.get("routes", [])
                ):
                    desc = d.get("description", "No details available")
                    disruptions.append(
                        f"- {d.get('title')}: {desc[:200]}{'...' if len(desc) > 200 else ''}"
                    )

        if not disruptions:
            return f"No current disruptions on {matched_line} line."

        return f"Current disruptions on {matched_line} line:<br>" + "<br>".join(disruptions)

    except requests.RequestException as e:
        return f"Error contacting disruptions API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
