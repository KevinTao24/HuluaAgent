from typing import List, Type

from hulua.tools.base import BaseTool
from hulua.tools.code import Code
from hulua.tools.google_serper import GoogleSerperTool
from hulua.tools.image import Image
from hulua.tools.search import Search


def get_default_tool() -> Type[BaseTool]:
    return GoogleSerperTool


def get_default_tool_name() -> str:
    tool = get_default_tool()
    return tool.name


def get_default_tools() -> List[Type[BaseTool]]:
    return [
        GoogleSerperTool,
    ]


def get_default_tools_names() -> List[str]:
    return [tool.name for tool in get_default_tools()]


def get_external_tools() -> List[Type[BaseTool]]:
    return []


def get_external_tools_names() -> List[str]:
    return [tool.name for tool in get_external_tools()]


def get_available_tools() -> List[Type[BaseTool]]:
    return get_default_tools() + get_external_tools()


def get_available_tools_names() -> List[str]:
    return get_default_tools_names() + get_external_tools_names()


def get_tool_name(tool: Type[BaseTool]) -> str:
    return format_tool_name(tool.__name__)


def format_tool_name(tool_name: str) -> str:
    return tool_name.lower()


def get_tool_from_name(tool_name: str) -> Type[BaseTool]:
    for tool in get_available_tools():
        if get_tool_name(tool) == format_tool_name(tool_name):
            return tool

    return get_default_tool()
