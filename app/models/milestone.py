from typing import List
from typing import Optional
from pydantic import BaseModel, Field


class CompletionRule(BaseModel):
    method: str
    required: bool = True


class Milestone(BaseModel):
    id: str

    title: str

    description: str

    depends_on: List[str] = Field(default_factory=list)

    skill_ids: List[str] = Field(default_factory=list)

    resource_ids: List[str] = Field(default_factory=list)

    exercise_ids: list[str] = Field(default_factory=list)

    assessment_id: str | None = None

    completion: CompletionRule