from datetime import datetime

from pydantic import BaseModel, Field


class StudyProgress(BaseModel):

    completed_objectives: list[str] = Field(default_factory=list)

    completed_exercises: list[str] = Field(default_factory=list)

    assessment_completed: bool = False

    started_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)