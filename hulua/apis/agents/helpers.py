from typing import Any, Callable, Dict, TypeVar

from langchain import BasePromptTemplate, LLMChain
from langchain.schema import BaseOutputParser, OutputParserException

# from langchain.chat_models.base import BaseChatModel
from langchain_core.language_models.chat_models import BaseChatModel

from hulua.schema.agent import ModelSettings

T = TypeVar("T")


def parse_with_handling(parser: BaseOutputParser[T], completion: str) -> T:
    try:
        return parser.parse(completion)
    except Exception as e:
        return "Big model api is experiencing issues."


async def call_model_with_handling(
    model: BaseChatModel,
    prompt: BasePromptTemplate,
    *args: Dict[str, str],
    settings: ModelSettings,
    **kwargs: Any,
) -> str:
    chain = LLMChain(llm=model, prompt=prompt)
    try:
        return await chain.arun(*args, **kwargs)
    except Exception as e:
        return "Big model api is experiencing issues."
