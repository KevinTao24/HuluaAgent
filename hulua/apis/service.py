from fastapi import APIRouter, Body, Depends
from fastapi.responses import StreamingResponse

from hulua.agents.agent import SummarizeAgent
from hulua.agents_services.base import BaseAgentService
from hulua.apis.depends import get_agent_service

router = APIRouter()


@router.post("/summarize")
async def summarize(
    req_body: SummarizeAgent = Body(...),
    agent_service: BaseAgentService = Depends(get_agent_service),
) -> StreamingResponse:
    return await agent_service.summarize_task_agent(
        goal=req_body.goal or "",
        results=req_body.results,
    )
