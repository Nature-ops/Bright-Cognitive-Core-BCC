from pydantic import BaseModel, Field


class ObjectiveAssessmentEvidence(BaseModel):
    """Explicit objective-level facts from one assessment attempt."""

    assessed_objective_ids: list[str] = Field(default_factory=list)
    successful_objective_ids: list[str] = Field(default_factory=list)
