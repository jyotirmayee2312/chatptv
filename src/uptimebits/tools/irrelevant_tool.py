# train_assistant/tools/irrelevant_tool.py

from langchain.tools import tool
from functions.irrelevant_handler import respond_to_irrelevant_query


@tool
def handle_irrelevant_query(input: str) -> str:
    """
    Tool: Respond to queries unrelated to train services in victoria.
    """
    return respond_to_irrelevant_query()

# train_assistant/tools/irrelevant_tool.py

