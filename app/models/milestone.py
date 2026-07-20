from typing import List

from pydantic import BaseModel, Field


class CompletionRule(BaseModel):
    method: str
    required: bool = True


class Milestone(BaseModel):
    id: str

    title: str

    description: str

    depends_on: List[str] = Field(default_factory=list)

    skills: List[str] = Field(default_factory=list)

    resources: List[str] = Field(default_factory=list)

    completion: CompletionRule