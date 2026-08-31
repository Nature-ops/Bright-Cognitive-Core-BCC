from pydantic import BaseModel, Field

from app.models.assessment_remediation import AssessmentRemediation


class AssessmentResult(BaseModel):

    assessment_id: str

    answers: dict[str, str] = Field(
        default_factory=dict
    )

    correct_answers: int = 0

    total_questions: int = 0

    score: float = 0.0

    passed: bool = False

    incorrect_question_ids: list[str] = Field(
        default_factory=list
    )

    remediation: list[AssessmentRemediation] = Field(
        default_factory=list
    )
