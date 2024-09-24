from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from hulua.schema.model import ModelSettings

Loop_Step = Literal[
    "start",
    "analyze",
    "execute",
    "create",
    "summarize",
    "chat",
]


class BaseAgent(BaseModel):
    goal: str
    model_settings: ModelSettings = Field(default=ModelSettings())


class StartAgent(BaseAgent):
    run_id: str


class TaskAnalyzeAgent(StartAgent):
    task: str
    tool_names: List[str] = Field(default=[])


class TaskExecuteAgent(StartAgent):
    task: str
    analysis: str


class TaskCreateAgent(StartAgent):
    tasks: List[str] = Field(default=[])
    last_task: Optional[str] = Field(default=None)
    result: Optional[str] = Field(default=None)
    completed_tasks: List[str] = Field(default=[])


class SummarizeAgent(StartAgent):
    results: List[str] = Field(default=[])


class ChatAgent(StartAgent):
    message: str
    results: List[str] = Field(default=[])


class NewTasksResponse(BaseModel):
    run_id: str
    new_tasks: List[str] = Field(alias="newTasks")


class RunCount(BaseModel):
    count: int
    first_run: Optional[datetime]
    last_run: Optional[datetime]
