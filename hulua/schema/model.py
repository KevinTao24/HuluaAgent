from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field, validator

LLM_Model = Literal["gpt-4o", "glm-4"]
LLM_MODEL_MAX_TOKENS: Dict[LLM_Model, int] = {"gpt-4o": 12800, "glm-4": 8000}


class ModelSettings(BaseModel):
    model: LLM_Model = Field(default="glm-4")
    custom_api_key: Optional[str] = Field(
        default="585f2d5ddf103304729767c75ab08094.uStCbbMiva4xxPTJ"
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
