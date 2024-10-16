from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field, validator

LLM_Model = Literal["gpt-4o", "glm-4", "glm-4-plus"]
LLM_MODEL_MAX_TOKENS: Dict[LLM_Model, int] = {
    "gpt-4o": 12800,
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
