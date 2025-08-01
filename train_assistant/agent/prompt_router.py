# train_assistant/agent/prompt_router.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

router_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a router assistant that chooses the best tool to answer questions about Melbourne trains."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
