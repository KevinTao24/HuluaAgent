from typing import Dict

from pydantic import BaseModel, validator

from hulua.tools.google_serper import GoogleSerperTool
from hulua.tools.tools import (
    get_available_tools_names,
    get_default_tool_name,
    get_tool_name,
)


class AnalysisArguments(BaseModel):
    """
    Arguments for the analysis function of a tool. OpenAI functions will resolve these values but leave out the action.
    """

    reasoning: str
    arg: str


class Analysis(AnalysisArguments):
    action: str

    @validator("action")
    def action_must_be_valid_tool(cls, v: str) -> str:
        if v not in get_available_tools_names():
            raise ValueError(f"Analysis action '{v}' is not a valid tool")
        return v

    @validator("action")
    def search_action_must_have_arg(cls, v: str, values: Dict[str, str]) -> str:
        if v == get_tool_name(GoogleSerperTool) and not values["arg"]:
            raise ValueError("Analysis arg cannot be empty if action is 'search'")
        return v

    @classmethod
    def get_default_analysis(cls, task: str) -> "Analysis":
        return cls(
            reasoning="Hmm... I'll try searching it up",
            action=get_default_tool_name(),
            arg=task,
        )
