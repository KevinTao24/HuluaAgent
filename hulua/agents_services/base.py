from typing import List, Optional, Protocol

from fastapi.responses import StreamingResponse


class BaseAgentService(Protocol):
    async def start_goal_agent(self, *, goal: str) -> List[str]:
        pass

    async def analyze_task_agent(
        self, *, goal: str, task: str, tool_names: List[str]
    ) -> str:
        pass

    async def execute_task_agent(
        self,
        *,
        goal: str,
        task: str,
        analysis: str,
    ) -> StreamingResponse:
        pass

    async def create_tasks_agent(
        self,
        *,
        goal: str,
        tasks: List[str],
        last_task: str,
        result: str,
        completed_tasks: Optional[List[str]] = None,
    ) -> List[str]:
        pass

    async def summarize_task_agent(
        self,
        *,
        goal: str,
        results: List[str],
    ) -> StreamingResponse:
        pass

    async def chat(
        self,
        *,
        message: str,
        results: List[str],
    ) -> StreamingResponse:
        pass
