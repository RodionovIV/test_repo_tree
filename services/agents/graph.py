import inspect
import re
import json
from typing import Literal, List

from langgraph.graph import StateGraph, END
from langgraph.types import Command

from services.agents.agent_state import AgentState
from services.agents.orchestrator_agent import OrchestratorAgent
from services.agents.AnalyticAgent_agent import AnalyticagentAgent

def parse_question(text: str) -> List[str]:
    """
    Извлекает все блоки JSON, заключённые в ```json ... ``` из текста.
    Возвращает список строк (каждая — отдельный блок JSON).
    """
    pattern = r"```json\s*(.*?)\s*```"
    matches = re.search(pattern, text, re.DOTALL)
    result = None
    if matches:
        result = eval(matches.group(1))
    return result

def orchestrator_node(agent):
    async def create_node(state:AgentState)->Command[Literal["AnalyticAgent", END]]:
        node_name = "orchestrator_node"
        task_field = "orchestrator_task"
        result_field = "orchestrator_result"
        state["previous"] = "orchestrator"
        print(f"Status: {node_name}")
        for _ in range(3):
            new_state = await agent.run_agent(state)
            tmp_result = parse_question(new_state[result_field])
            if tmp_result:
                new_state[result_field] = tmp_result["result"]
                goto = tmp_result["next"]
                break
        else:
            new_state[result_field] = "FAIL"
            goto = "END"
        if goto == "END":
            new_state["result"] = new_state[result_field]
            goto = END
        return Command(
            update={
                k:v for k, v in new_state.items()
            },
            goto=goto
        )
    return create_node



def AnalyticAgent_node(agent):
    async def create_node(state:AgentState)->Command[Literal["orchestrator"]]:
        node_name = "AnalyticAgent_node"
        task_field = "AnalyticAgent_task"
        result_field = "AnalyticAgent_result"
        state["previous"] = "AnalyticAgent"
        print(f"Status: {node_name}")

        new_state = await agent.run_agent(state)

        goto = "orchestrator"
        if goto == END:
            new_state["result"] = new_state[result_field]
        return Command(
            update={
                k:v for k, v in new_state.items()
            },
            goto=goto
        )
    return create_node


async def create_graph():
    _orchestrator_agent = OrchestratorAgent()
    await _orchestrator_agent.create()
    _AnalyticAgent_agent = AnalyticagentAgent()
    await _AnalyticAgent_agent.create()
    builder = StateGraph(state_schema=AgentState)
    builder.set_entry_point("orchestrator")
    builder.add_node("orchestrator", orchestrator_node(_orchestrator_agent))
    builder.add_node("AnalyticAgent", AnalyticAgent_node(_AnalyticAgent_agent))
    graph = builder.compile()
    return graph