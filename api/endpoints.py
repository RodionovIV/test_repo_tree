from fastapi import APIRouter
from models.agents import AgentRequest, AgentResponse
from services.agents.graph import create_graph
from services.agents.agent_state import AgentState


router = APIRouter()

@router.post("/run_agent", response_model=AgentResponse)
async def process_agent_request(request: AgentRequest):
    graph = await create_graph()
    state = AgentState(**{"orchestrator_task": request.query})
    result_state = await graph.ainvoke(state)
    result = result_state["result"]
    return AgentResponse(result=result)