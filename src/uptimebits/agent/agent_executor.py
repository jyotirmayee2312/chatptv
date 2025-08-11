# train_assistant/agent/agent_executor.py

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_aws import ChatBedrock
from agent.prompt_router import router_prompt
from agent.tool_router import tools

llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="ap-southeast-2",
)

router_agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=router_prompt,
)

agent_executor = AgentExecutor(
    agent=router_agent,
    tools=tools,
    verbose=True,
)
