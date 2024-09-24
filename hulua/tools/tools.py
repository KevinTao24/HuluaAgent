from typing import List, Type

from hulua.tools.base import BaseTool
from hulua.tools.google_serper import GoogleSerperTool


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
