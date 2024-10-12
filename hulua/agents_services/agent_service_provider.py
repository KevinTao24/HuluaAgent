from typing import Any, Callable, Coroutine, Optional

from fastapi import Depends

from hulua.agents.model_factory import create_model_glm
from hulua.agents_services.agent_service import AgentService
from hulua.agents_services.mock_agent_service import MockAgentService

# from hulua.agents_services.openai_agent_service import (
#     OpenAIAgentService,
# )
from hulua.agents_services.zhipu_agent_service import ZhipuAgentService
from hulua.schema.agent import AgentRun, LLM_Model
from hulua.settings import settings


def get_agent_service(
    validator: Callable[..., Coroutine[Any, Any, AgentRun]],
    streaming: bool = False,
    llm_model: Optional[LLM_Model] = None,
) -> Callable[..., AgentService]:
    def func(
        run: AgentRun = Depends(validator),
    ) -> AgentService:
        if settings.ff_mock_mode_enabled:
            return MockAgentService()

        model = create_model_glm(
            settings,
            run.model_settings,
            streaming=streaming,
            force_model=llm_model,
        )

        return ZhipuAgentService(model, run.model_settings, callbacks=None)

    return func
