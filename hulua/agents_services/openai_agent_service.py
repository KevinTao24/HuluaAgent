from typing import List, Optional

import tiktoken
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from lanarky.responses import StreamingResponse
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.chains.llm import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.schema import HumanMessage
from loguru import logger
from pydantic import ValidationError
from reworkd_platform.web.api.agent.analysis import Analysis, AnalysisArguments
from reworkd_platform.web.api.agent.helpers import (
    call_model_with_handling,
    openai_error_handler,
    parse_with_handling,
)
from reworkd_platform.web.api.agent.model_factory import WrappedChatOpenAI
from reworkd_platform.web.api.agent.prompts import (
    analyze_task_prompt,
    chat_prompt,
    create_tasks_prompt,
    start_goal_prompt,
)
from reworkd_platform.web.api.agent.tools.open_ai_function import get_tool_function
from reworkd_platform.web.api.agent.tools.utils import summarize

from hulua.agents_services.base import BaseAgentService
from hulua.outputs.task_output_parser import TaskOutputParser
from hulua.schema.model import ModelSettings
from hulua.tools.tools import (
    get_default_tool,
    get_default_tool_name,
    get_external_tools,
)

encoding = tiktoken.get_encoding("cl100k_base")


class OpenAIAgentService(BaseAgentService):
    def __init__(
        self,
        model: WrappedChatOpenAI,
        settings: ModelSettings,
        callbacks: Optional[List[AsyncCallbackHandler]],
    ):
        self.model = model
        self.settings = settings
        self.callbacks = callbacks

    async def start_goal_agent(self, *, goal: str) -> List[str]:
        prompt = ChatPromptTemplate.from_messages(
            [SystemMessagePromptTemplate(prompt=start_goal_prompt)]
        )

        completion = await call_model_with_handling(
            self.model,
            ChatPromptTemplate.from_messages(
                [SystemMessagePromptTemplate(prompt=start_goal_prompt)]
            ),
            {"goal": goal, "language": self.settings.language},
            settings=self.settings,
            callbacks=self.callbacks,
        )

        task_output_parser = TaskOutputParser(completed_tasks=[])
        tasks = parse_with_handling(task_output_parser, completion)

        return tasks

    async def analyze_task_agent(
        self, *, goal: str, task: str, tool_names: List[str]
    ) -> Analysis:
        user_tools = await get_user_tools(tool_names, self.user, self.oauth_crud)
        functions = list(map(get_tool_function, user_tools))
        prompt = analyze_task_prompt.format_prompt(
            goal=goal,
            task=task,
            language=self.settings.language,
        )

        message = await openai_error_handler(
            func=self.model.apredict_messages,
            messages=prompt.to_messages(),
            functions=functions,
            settings=self.settings,
            callbacks=self.callbacks,
        )

        function_call = message.additional_kwargs.get("function_call", {})
        completion = function_call.get("arguments", "")

        try:
            pydantic_parser = PydanticOutputParser(pydantic_object=AnalysisArguments)
            analysis_arguments = parse_with_handling(pydantic_parser, completion)
            return Analysis(
                action=function_call.get("name", get_tool_name(get_default_tool())),
                **analysis_arguments.dict(),
            )
        except ValidationError:
            return Analysis.get_default_analysis(task)

    async def execute_task_agent(
        self,
        *,
        goal: str,
        task: str,
        analysis: Analysis,
    ) -> StreamingResponse:
        # TODO: More mature way of calculating max_tokens
        if self.model.max_tokens > 3000:
            self.model.max_tokens = max(self.model.max_tokens - 1000, 3000)

        tool_class = get_tool_from_name(analysis.action)
        return await tool_class(self.model, self.settings.language).call(
            goal,
            task,
            analysis.arg,
            self.user,
            self.oauth_crud,
        )

    async def create_tasks_agent(
        self,
        *,
        goal: str,
        tasks: List[str],
        last_task: str,
        result: str,
        completed_tasks: Optional[List[str]] = None,
    ) -> List[str]:
        prompt = ChatPromptTemplate.from_messages(
            [SystemMessagePromptTemplate(prompt=create_tasks_prompt)]
        )

        args = {
            "goal": goal,
            "language": self.settings.language,
            "tasks": "\n".join(tasks),
            "lastTask": last_task,
            "result": result,
        }

        completion = await call_model_with_handling(
            self.model, prompt, args, settings=self.settings, callbacks=self.callbacks
        )

        previous_tasks = (completed_tasks or []) + tasks
        return [completion] if completion not in previous_tasks else []

    async def summarize_task_agent(
        self,
        *,
        goal: str,
        results: List[str],
    ) -> FastAPIStreamingResponse:
        self.model.model_name = "gpt-3.5-turbo-16k"
        self.model.max_tokens = 8000  # Total tokens = prompt tokens + completion tokens

        snippet_max_tokens = 7000  # Leave room for the rest of the prompt
        text_tokens = encoding.encode("".join(results))
        text = encoding.decode(text_tokens[0:snippet_max_tokens])
        logger.info(f"Summarizing text: {text}")

        return summarize(
            model=self.model,
            language=self.settings.language,
            goal=goal,
            text=text,
        )

    async def chat(
        self,
        *,
        message: str,
        results: List[str],
    ) -> FastAPIStreamingResponse:
        self.model.model_name = "gpt-3.5-turbo-16k"
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate(prompt=chat_prompt),
                *[HumanMessage(content=result) for result in results],
                HumanMessage(content=message),
            ]
        )

        chain = LLMChain(llm=self.model, prompt=prompt)

        return StreamingResponse.from_chain(
            chain,
            {"language": self.settings.language},
            media_type="text/event-stream",
        )
