# train_assistant/agent/prompt_router.py

# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# router_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a router assistant that chooses the best tool to answer questions about Melbourne trains."),
#     ("user", "{input}"),
#     MessagesPlaceholder(variable_name="agent_scratchpad"),
# ])

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

router_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a smart and concise Melbourne train travel assistant. "
     "Your job is to decide which tool to use based on what the user asks. "
     "Users may ask in simple or open-ended ways, so infer their intent clearly. "
     "Keep responses short, helpful, and focused. "
     "If user gives only one value and it looks like a line (e.g., 'Belgrave line'), "
     "assume they are asking about disruptions on that line. "
     "Do not make up answers; always use a tool. "
     "Do not reroute users, just return the tool’s answer."
    ),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

