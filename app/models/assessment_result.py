from datetime import UTC, datetime

from pydantic import BaseModel


class AssessmentResult(BaseModel):
    assessment_id: str

    score: float = 0.0

    passed: bool = False

    completed_at: datetime | None = None