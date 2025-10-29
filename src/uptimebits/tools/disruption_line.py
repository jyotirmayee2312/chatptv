# tools/disruption_line.py
# from langchain.tools import tool
from strands import tool
from pydantic import BaseModel, Field
from typing import Optional
import importlib.resources as pkg_resources
import json
import boto3
import os

# import functions
from functions.disruption_line import _check_disruptions_on_line, _search_across_types

# # Load route_reference.json for help messages
# with pkg_resources.files("context").joinpath("route_reference.json").open("r", encoding="utf-8") as f:
#     ROUTE_DATA = json.load(f)

# Load route_reference.json from S3
s3 = boto3.client("s3")
bucket = os.environ.get("CHAT_HISTORY_BUCKET", "chathistorybucket-chatbuddy")
key = "route_reference/route_reference.json"

obj = s3.get_object(Bucket=bucket, Key=key)
ROUTE_DATA = json.loads(obj["Body"].read().decode("utf-8"))


class LineDisruptionInput(BaseModel):
    route_type: Optional[int] = Field(
        None,
        description="0 = Metro trains, 3 = V/Line trains"
    )
    line_name: Optional[str] = Field(
        None,
        description="The name of the line (e.g. 'Craigieburn')."
    )


@tool
def check_disruptions_from_line(route_type: Optional[int] = None, line_name: Optional[str] = None) -> str:
    """
    LangChain tool wrapper — validates inputs and delegates to functions/disruption_line.
    Always routes through _check_disruptions_on_line to allow fuzzy matching.
    """
    if not line_name:
        if route_type == ROUTE_DATA.get("metro", {}).get("route_type"):
            return f"Please provide a metro line name. Options: {', '.join(ROUTE_DATA['metro']['lines'])}"
        elif route_type == ROUTE_DATA.get("vline", {}).get("route_type"):
            return f"Please provide a V/Line line name. Options: {', '.join(ROUTE_DATA['vline']['lines'])}"
        else:
            return (
                f"Please provide a line name. "
                f"Available Metro lines: {', '.join(ROUTE_DATA['metro']['lines'])}. "
                f"Available V/Line lines: {', '.join(ROUTE_DATA['vline']['lines'])}."
            )

    # Always delegate to function so fuzzy match runs
    if route_type in [
        ROUTE_DATA.get("metro", {}).get("route_type"),
        ROUTE_DATA.get("vline", {}).get("route_type")
    ]:
        return _check_disruptions_on_line(line_name, route_type)

    # Auto-detect across both if route_type not specified
    fallback_match, fallback_type = _search_across_types(line_name)
    if fallback_match and fallback_type is not None:
        return _check_disruptions_on_line(fallback_match, fallback_type)

    return f"No line found for '{line_name}' in metro or V/Line routes."
