# train_assistant/agent/tool_router.py

from tools.timetable_tool import train_tool
from tools.disruption_tool import check_disruptions_from_route
from tools.irrelevant_tool import handle_irrelevant_query
from tools.disruption_line import check_disruptions_from_line

# train_assistant/agent/tool_router.py
from tools.vline_timetable_tool import vline_train_tool
from tools.combined_timetable_tool import combined_timetable_tool
from tools.chat_history import json_qa_tool


tools = [
    train_tool,
    check_disruptions_from_route,
    check_disruptions_from_line,
    handle_irrelevant_query,
    vline_train_tool,
    combined_timetable_tool,
    json_qa_tool
]

