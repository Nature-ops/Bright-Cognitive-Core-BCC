from datetime import UTC, datetime
from pydantic import BaseModel


class ExerciseResult(BaseModel):
    exercise_id: str

    completed: bool = False

    completed_at: datetime | None = None

    notes: str = ""