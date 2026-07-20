from typing import List

from pydantic import BaseModel, Field


class GoalTemplate(BaseModel):
    title: str
    description: str
    success_criteria: List[str] = Field(default_factory=list)