# train_assistant/agent/tool_router.py

from tools.timetable_tool import train_tool
from tools.disruption_tool import check_disruptions_from_route
from tools.irrelevant_tool import handle_irrelevant_query
from tools.disruption_line import check_disruptions_from_line

tools = [train_tool, check_disruptions_from_route, check_disruptions_from_line, handle_irrelevant_query]
# train_assistant/agent/tool_router.py

