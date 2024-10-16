from dataclasses import dataclass
from typing import List

from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from lanarky.responses import StreamingResponse
from langchain.chains.llm import LLMChain
from langchain.chat_models.base import BaseChatModel


@dataclass
class CitedSnippet:
    index: int
    text: str
    url: str = ""

    def __repr__(self) -> str:
        """
        The string representation the AI model will see
        """
        return f"{{i: {self.index}, text: {self.text}, url: {self.url}}}"


@dataclass
class Snippet:
    text: str

    def __repr__(self) -> str:
        """
        The string representation the AI model will see
        """
        return f"{{text: {self.text}}}"


def summarize_with_sources(
    model: BaseChatModel,
    language: str,
    goal: str,
    query: str,
    snippets: List[CitedSnippet],
) -> FastAPIStreamingResponse:
    from hulua.apis.agents.prompts import summarize_with_sources_prompt

    chain = LLMChain(llm=model, prompt=summarize_with_sources_prompt)

    return StreamingResponse.from_chain(
        chain,
        {
            "goal": goal,
            "query": query,
            "language": language,
            "snippets": snippets,
        },
        media_type="text/event-stream",
    )
