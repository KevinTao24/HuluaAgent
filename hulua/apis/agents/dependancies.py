from typing import TypeVar

from fastapi import Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hulua.schema.agent import (
    AgentChat,
    AgentRun,
    AgentRunCreate,
    AgentSummarize,
    AgentTaskAnalyze,
    AgentTaskCreate,
    AgentTaskExecute,
)

T = TypeVar(
    "T", AgentTaskAnalyze, AgentTaskExecute, AgentTaskCreate, AgentSummarize, AgentChat
)


# def agent_crud(
#     user: UserBase = Depends(get_current_user),
#     session: AsyncSession = Depends(get_db_session),
# ) -> AgentCRUD:
#     return AgentCRUD(session, user)


async def agent_start_validator(
    body: AgentRunCreate = Body(
        example={
            "goal": "Create business plan for a bagel company",
            "modelSettings": {
                "customModelName": "gpt-3.5-turbo",
            },
        },
    )
) -> AgentRun:
    return AgentRun(**body.dict(), run_id=str("default_id"))


# async def validate(body: T, crud: AgentCRUD, type_: Loop_Step) -> T:
#     body.run_id = (await crud.create_task(body.run_id, type_)).id
#     return body


async def agent_analyze_validator(
    body: AgentTaskAnalyze = Body(),
) -> AgentTaskAnalyze:
    # body.run_id = str("default_id")
    return AgentTaskAnalyze(**body.dict())


async def agent_execute_validator(
    body: AgentTaskExecute = Body(
        example={
            "goal": "Perform tasks accurately",
            "task": "Write code to make a platformer",
            "analysis": {
                "reasoning": "I like to write code.",
                "action": "code",
                "arg": "",
            },
        },
    )
) -> AgentTaskExecute:
    return AgentTaskExecute(**body.dict())


async def agent_create_validator(body: AgentTaskCreate = Body()) -> AgentTaskCreate:
    return AgentTaskCreate(**body.dict())


async def agent_summarize_validator(
    body: AgentSummarize = Body(),
) -> AgentSummarize:
    return AgentSummarize(**body.dict())


async def agent_chat_validator(
    body: AgentChat = Body(),
) -> AgentChat:
    return AgentChat(**body.dict())
