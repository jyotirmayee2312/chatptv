# train_assistant/agent/agent_executor.py

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_aws import ChatBedrock
from agent.prompt_router import router_prompt
from agent.tool_router import tools
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
import json
from strands import tool,Agent
llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="ap-southeast-2",
)

# router_agent = create_tool_calling_agent(
#     llm=llm,
#     tools=tools,
#     prompt=router_prompt,
# )

# # agent_executor = AgentExecutor(
# #     agent=router_agent,
# #     tools=tools,
# #     verbose=True,
# # )

# agent_executor = AgentExecutor(
#     agent=router_agent,
#     tools=tools,
#     verbose=True,  # Now using the correct memory type
#     return_intermediate_steps=False
# )

def create_agent_with_tools(custom_tools):
    """Create agent executor with custom tools."""
    # router_agent = create_tool_calling_agent(
    #     llm=llm,
    #     tools=custom_tools,
    #     prompt=router_prompt,
    # )
    
    # return AgentExecutor(
    #     agent=router_agent,
    #     tools=custom_tools,
    #     verbose=True,
    #     return_intermediate_steps=False
    # )
    return Agent(
    system_prompt=router_prompt,
    model="anthropic.claude-3-haiku-20240307-v1:0",
    tools=custom_tools,
    # state={"actor_id": actor_id, "session_id": session_id}
)
    
