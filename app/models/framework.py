from typing import List

from pydantic import BaseModel, Field

from app.models.milestone import Milestone
from app.models.goal_template import GoalTemplate




class Framework(BaseModel):
    id: str

    name: str

    version: str

    domain: str

    description: str

    difficulty: str

    estimated_duration: str

    tags: List[str] = Field(default_factory=list)

    goal_template: GoalTemplate

    milestones: List[Milestone] = Field(default_factory=list)