from datetime import datetime, UTC

from pydantic import BaseModel, Field


class StudyProgress(BaseModel):

    session_id: str

    completed_objectives: list[str] = Field(default_factory=list)

    completed_exercises: list[str] = Field(default_factory=list)

    assessment_completed: bool = False

    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))