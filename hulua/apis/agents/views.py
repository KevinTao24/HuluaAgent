from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Form
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from pydantic import BaseModel

from hulua.agents_services.agent_service import AgentService
from hulua.agents_services.agent_service_provider import get_agent_service
from hulua.apis.agents.analysis import Analysis
from hulua.apis.agents.dependancies import (
    agent_analyze_validator,
    agent_chat_validator,
    agent_create_validator,
    agent_execute_validator,
    agent_start_validator,
    agent_summarize_validator,
)
from hulua.schema.agent import (
    AgentChat,
    AgentRun,
    AgentSummarize,
    AgentTaskAnalyze,
    AgentTaskCreate,
    AgentTaskExecute,
    NewTasksResponse,
)
from hulua.tools.tools import get_external_tools, get_tool_name

# from reworkd_platform.web.api.agent.dependancies import (
#     agent_analyze_validator,
#     agent_chat_validator,
#     agent_create_validator,
#     agent_execute_validator,
#     agent_start_validator,
#     agent_summarize_validator,
# )
router = APIRouter()
# from reworkd_platform.web.api.agent.agent_service.agent_service_provider import (
#     get_agent_service,
# )


@router.post("/start")
async def start_tasks(
    req_body=Depends(agent_start_validator),
    agent_service=Depends(get_agent_service(agent_start_validator)),
) -> NewTasksResponse:
    new_tasks = await agent_service.start_goal_agent(goal=req_body.goal)
    return NewTasksResponse(newTasks=new_tasks, run_id=req_body.run_id)


@router.post("/analyze")
async def analyze_tasks(
    req_body=Depends(agent_analyze_validator),
    agent_service=Depends(get_agent_service(agent_analyze_validator)),
) -> Analysis:
    return await agent_service.analyze_task_agent(
        goal=req_body.goal,
        task=req_body.task or "",
        tool_names=req_body.tool_names or [],
    )


@router.post("/execute")
async def execute_tasks(
    req_body=Depends(agent_execute_validator),
    agent_service=Depends(get_agent_service(agent_execute_validator, streaming=True)),
) -> FastAPIStreamingResponse:
    return await agent_service.execute_task_agent(
        goal=req_body.goal or "",
        task=req_body.task or "",
        analysis=req_body.analysis,
    )


@router.post("/create")
async def create_tasks(
    req_body=Depends(agent_create_validator),
    agent_service=Depends(get_agent_service(agent_create_validator)),
) -> NewTasksResponse:
    new_tasks = await agent_service.create_tasks_agent(
        goal=req_body.goal,
        tasks=req_body.tasks or [],
        last_task=req_body.last_task or "",
        result=req_body.result or "",
        completed_tasks=req_body.completed_tasks or [],
    )
    return NewTasksResponse(newTasks=new_tasks, run_id=req_body.run_id)


@router.post("/summarize")
async def summarize(
    req_body=Depends(agent_summarize_validator),
    agent_service=Depends(
        get_agent_service(
            validator=agent_summarize_validator,
            streaming=True,
        )
    ),
) -> FastAPIStreamingResponse:
    return await agent_service.summarize_task_agent(
        goal=req_body.goal or "",
        results=req_body.results,
    )


@router.post("/chat")
async def chat(
    req_body=Depends(agent_chat_validator),
    agent_service=Depends(
        get_agent_service(
            validator=agent_chat_validator,
            streaming=True,
            llm_model="gpt-3.5-turbo-16k",
        ),
    ),
) -> FastAPIStreamingResponse:
    return await agent_service.chat(
        message=req_body.message,
        results=req_body.results,
    )


@router.post("/ques")
async def ques(body: Dict) -> FastAPIStreamingResponse:
    from langchain_core.messages import (
        AIMessage,
        BaseMessage,
        HumanMessage,
        SystemMessage,
        ToolMessage,
    )

    from hulua.agents_services.zhipu import ChatZhipuAI

    llm = ChatZhipuAI(
        api_key="5883dd03650ccbfd219da66b3832e0ef.UuJtNmuEj5S9mROb", model="glm-4-plus"
    )
    candi = body.get("candi", "")
    if isinstance(candi, str):
        candi = eval(candi)
    ques_list = candi.keys()
    index = len(ques_list)
    if index >= 8:
        prompt = """你是一名保险代理人面试官，目标是选出潜在的绩优代理人，已知候选人的资料如下：【{candi}】,需要以面试官的口吻提出10个问题来全面了解代理人信息，当前是第{index}个问题，类型为问答题，你需要只输出问题本身，不需要包含题号，以列表的形式展示，如[""]，问题如下："""
    else:
        prompt = """你是一名保险代理人面试官，目标是选出潜在的绩优代理人，已知候选人的资料如下：【{candi}】,需要以面试官的口吻提出10个问题来全面了解代理人信息，当前是第{index}个问题，类型为选择题，你需要只输出问题本身和4个选项，不需要包含选项标识和题号，以列表的形式展示，如["","","","",""]，问题如下："""
    messages = [
        SystemMessage(content="你是一个小说家"),
        HumanMessage(content=prompt.format(candi=candi, index=index)),
    ]
    result = {
        "code": 200,
        "message": "success",
        "result": llm._generate(messages)
        .dict()
        .get("generations", [{}])[0]
        .get("text", {}),
    }

    return result


class ToolModel(BaseModel):
    name: str
    description: str
    color: str
    image_url: Optional[str]


class ToolsResponse(BaseModel):
    tools: List[ToolModel]


@router.get("/tools")
async def get_user_tools() -> ToolsResponse:
    tools = get_external_tools()
    formatted_tools = [
        ToolModel(
            name=get_tool_name(tool),
            description=tool.public_description,
            color="TODO: Change to image of tool",
            image_url=tool.image_url,
        )
        for tool in tools
        if tool.available()
    ]

    return ToolsResponse(tools=formatted_tools)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(router, host="0.0.0.0", port=30080)
