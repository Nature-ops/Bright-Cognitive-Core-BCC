from datetime import UTC, datetime

from pydantic import BaseModel, Field


class AssessmentEvidence(BaseModel):
    framework_id: str
    milestone_id: str
    assessment_id: str
    score: float
    passed: bool
    incorrect_question_ids: list[str] = Field(default_factory=list)
    learning_gap_objective_ids: list[str] = Field(default_factory=list)
    recorded_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
