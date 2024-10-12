from abc import ABC, abstractmethod
from typing import Optional

from lanarky.responses import StreamingResponse
from langchain.chat_models.base import BaseChatModel


class Tool(ABC):
    description: str = ""
    public_description: str = ""
    arg_description: str = "The argument to the function."
    image_url: str = "/tools/openai-white.png"

    model: BaseChatModel
    language: str

    def __init__(self, model: BaseChatModel = None, language: str = "简体中文"):
        self.model = model
        self.language = language

    @staticmethod
    def available() -> bool:
        return True

    @abstractmethod
    async def call(self, goal: str, task: str, input_str: str) -> StreamingResponse:
        pass
