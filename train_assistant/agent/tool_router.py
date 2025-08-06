# train_assistant/agent/tool_router.py

from train_assistant.tools.timetable_tool import train_tool
from train_assistant.tools.disruption_tool import check_disruptions_from_route
from train_assistant.tools.irrelevant_tool import handle_irrelevant_query
from train_assistant.tools.disruption_line import check_disruptions_from_line

tools = [train_tool, check_disruptions_from_route, check_disruptions_from_line, handle_irrelevant_query]
