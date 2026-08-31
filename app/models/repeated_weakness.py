from pydantic import BaseModel, Field


class RepeatedWeakness(BaseModel):
    """An objective missed in multiple historical assessment attempts."""

    framework_id: str
    objective_id: str
    missed_attempt_count: int
    source_assessment_ids: list[str] = Field(default_factory=list)
