from pydantic import BaseModel
from pydantic import Field
from app.models.framework import Framework
from app.models.milestone import Milestone
from app.models.objective import Objective
from app.models.resource import Resource
from app.models.skill import Skill


class LearningPlan(BaseModel):

    framework: Framework

    milestone: Milestone

    skills: list[Skill]

    resources: list[Resource]

    objectives: list[Objective] = Field(default_factory=list)