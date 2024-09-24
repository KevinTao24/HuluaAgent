import time
from typing import Any, List

from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from shared.utils.mock_streaming import streaming_string

from hulua.agents_services.base import BaseAgentService


class MockAgentService(BaseAgentService):
    async def start_goal_agent(self, **kwargs: Any) -> List[str]:
        time.sleep(1)
        return ["Task X", "Task Y", "Task Z"]

    async def create_tasks_agent(self, **kwargs: Any) -> List[str]:
        time.sleep(1)
        return ["Some random task that doesn't exist"]

    async def analyze_task_agent(self, **kwargs: Any) -> str:
        time.sleep(1.5)
        return str(
            action="reason",
            arg="Mock analysis",
            reasoning="Mock to avoid wasting money calling the OpenAI API.",
        )

    async def execute_task_agent(self, **kwargs: Any) -> FastAPIStreamingResponse:
        time.sleep(0.5)
        return streaming_string(
            """ This is going to be a longer task result such that
        We make the stream of this string take time and feel long. The reality is... this is a mock! 
        
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
        when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
        It has survived not only five centuries, but also the leap into electronic typesetting, remaining unchanged.
        """
            + kwargs.get("task", "task"),
            True,
        )

    async def summarize_task_agent(
        self,
        *,
        goal: str,
        results: List[str],
    ) -> FastAPIStreamingResponse:
        time.sleep(0.5)
        return streaming_string(
            """ This is going to be a longer task result such that
        We make the stream of this string take time and feel long. The reality is... this is a mock! 
        
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
        when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
        It has survived not only five centuries, but also the leap into electronic typesetting, remaining unchanged.
        """,
            True,
        )

    async def chat(
        self,
        *,
        message: str,
        results: List[str],
    ) -> FastAPIStreamingResponse:
        time.sleep(0.5)
        return streaming_string(
            "What do you want dude?",
            True,
        )