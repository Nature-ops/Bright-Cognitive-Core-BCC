from pydantic import BaseModel, Field


class AssessmentResult(BaseModel):

    assessment_id: str

    answers: dict[str, str] = Field(
        default_factory=dict
    )

    correct_answers: int = 0

    total_questions: int = 0

    score: float = 0.0

    passed: bool = False