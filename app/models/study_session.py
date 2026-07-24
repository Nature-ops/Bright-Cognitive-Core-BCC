from datetime import datetime

from pydantic import BaseModel, Field

from app.models.assessment import Assessment
from app.models.exercise import Exercise
from app.models.learning_plan import LearningPlan
from app.models.resource import Resource


class Objective(BaseModel):
    id: str
    title: str
    completed: bool = False


class StudySession(BaseModel):
    """
    Represents a complete learning session generated from a LearningPlan.
    """

    learning_plan: LearningPlan

    objectives: list[Objective] = Field(default_factory=list)

    resources: list[Resource] = Field(default_factory=list)

    exercises: list[Exercise] = Field(default_factory=list)

    assessment: Assessment | None = None

    estimated_minutes: int = 0

    created_at: datetime = Field(default_factory=datetime.utcnow)