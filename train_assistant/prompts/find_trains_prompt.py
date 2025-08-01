from langchain.prompts import PromptTemplate

find_trains_prompt = PromptTemplate.from_template(
    """You are a smart assistant helping users find train schedules.
Given a query about trains from one station to another, extract the station names and call the correct API tool.
Query: {input}
"""
)
