from langchain.agents import create_react_agent, AgentExecutor
from langchain_aws import ChatBedrock
from langchain.tools import Tool
from tools.find_trains import get_train_departures
from tools.check_disruptions import check_disruptions
from prompts.route_prompt import ROUTE_AGENT_PROMPT

from langchain_core.prompts import PromptTemplate


from langchain_core.prompts import PromptTemplate

ROUTE_AGENT_PROMPT = PromptTemplate.from_template("""
You are a helpful travel assistant. You have access to the following tools:

{tools}

Tool Names: {tool_names}

Use these tools to help users with questions related to train routes and disruptions.

Question: {input}

{agent_scratchpad}
""")




llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",  # Make sure this matches your model
    region_name="us-east-1",  # Or your AWS region
)

tools = [
    Tool(name="FindTrainRoute", func=get_train_departures, description="Get trains between two stations"),
    Tool(name="CheckDisruptions", func=check_disruptions, description="Check line disruptions")
]

agent = create_react_agent(llm=llm, tools=tools, prompt=ROUTE_AGENT_PROMPT)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_route_agent(user_input: str) -> str:
    return agent_executor.invoke({"input": user_input})