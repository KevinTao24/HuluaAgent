from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, validator

from hulua.apis.agents.analysis import Analysis

LLM_Model = Literal[
    "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "glm-4", "glm-4-plus"
]
Loop_Step = Literal[
    "start",
    "analyze",
    "execute",
    "create",
    "summarize",
    "chat",
]
LLM_MODEL_MAX_TOKENS: Dict[LLM_Model, int] = {
    "gpt-3.5-turbo": 4000,
    "gpt-3.5-turbo-16k": 16000,
    "gpt-4": 8000,
    "glm-4": 8000,
    "glm-4-plus": 16000,
}


class ModelSettings(BaseModel):
    model: LLM_Model = Field(default="glm-4-plus")
    custom_api_key: Optional[str] = Field(
        default="5883dd03650ccbfd219da66b3832e0ef.UuJtNmuEj5S9mROb"
    )
    temperature: float = Field(default=0.01, ge=0.0, le=1.0)
    max_tokens: int = Field(default=500, ge=0)
    language: str = Field(default="CHINESE")

    @validator("max_tokens")
    def validate_max_tokens(cls, v: float, values: Dict[str, Any]) -> float:
        model = values["model"]
        if v > (max_tokens := LLM_MODEL_MAX_TOKENS[model]):
            raise ValueError(f"Model {model} only supports {max_tokens} tokens")
        return v


class AgentRunCreate(BaseModel):
    goal: str
    model_settings: ModelSettings = Field(default=ModelSettings())


class AgentRun(AgentRunCreate):
    run_id: str


class AgentTaskAnalyze(AgentRun):
    task: str
    tool_names: List[str] = Field(default=[])
    model_settings: ModelSettings = Field(default=ModelSettings())


class AgentTaskExecute(AgentRun):
    task: str
    analysis: Analysis


class AgentTaskCreate(AgentRun):
    tasks: List[str] = Field(default=[])
    last_task: Optional[str] = Field(default=None)
    result: Optional[str] = Field(default=None)
    completed_tasks: List[str] = Field(default=[])


class AgentSummarize(AgentRun):
    results: List[str] = Field(default=[])


class AgentChat(AgentRun):
    message: str
    results: List[str] = Field(default=[])


class NewTasksResponse(BaseModel):
    run_id: str
    new_tasks: List[str] = Field(alias="newTasks")


class RunCount(BaseModel):
    count: int
    first_run: Optional[datetime]
    last_run: Optional[datetime]
