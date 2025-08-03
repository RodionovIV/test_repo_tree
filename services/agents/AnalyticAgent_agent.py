import logging
from uuid import uuid4

from langchain.schema import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from services.mcp.mcp_client import client
from settings import llm, AnalyticAgent_prompt
from services.agents.agent_state import AgentState

_LOGGER = logging.getLogger(__name__)


class AnalyticagentAgent:
    def __init__(self):
        pass

    async def create(self):
        tools = []
        for server_name in ['server_rag', 'server_web_search']:
            tools += await client.get_tools(server_name=server_name)
        self.agent = create_react_agent(llm, tools, checkpointer=MemorySaver(), prompt=AnalyticAgent_prompt)
        self.config = {
                "configurable": {
                "thread_id": str(uuid4())
            },
            "recursion_limit": 100
        }

    async def run_agent(self, state: AgentState):
        tread_id = self.config['configurable']['thread_id']
        class_name = self.__class__.__name__.lower()
        task_field = "AnalyticAgent_task"
        result_field = "AnalyticAgent_result"

        _LOGGER.info(f"Status: {class_name}, thread_id: {tread_id}")

        if "messages" in state and state["messages"]:
            old_messages = state["messages"]
            request = state["messages"][-1].content
        else:
            old_messages = []
            request = state[task_field]
        _LOGGER.info(f"{class_name} request: {request}")
        request = {"messages": [HumanMessage(content=request)]}
        response = await self.agent.ainvoke(request, config=self.config)
        if isinstance(response, dict):
            result = response["messages"][-1].content
        else:
            result = response
        _LOGGER.info(f"{class_name} response: {result}")
        state["messages"] = old_messages + [HumanMessage(content=result)]
        state[result_field] = result
        return state