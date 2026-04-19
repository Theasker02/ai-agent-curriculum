"""
Generic document extraction schema.

Adapt fields to your domain. The pipeline, LLM wrapper and HITL code do NOT
care about the specific fields — they only care that the schema is a Pydantic
model with a `confidence` float.
"""
from pydantic import BaseModel, Field


class Entity(BaseModel):
    kind: str = Field(description="Entity category, e.g. 'person', 'date', 'amount'")
    value: str
    span: str | None = Field(default=None, description="Original text span, optional")


class DocumentExtract(BaseModel):
    title: str
    summary: str = Field(description="Short summary, 1-3 sentences")
    entities: list[Entity] = Field(default_factory=list)
    key_points: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
