from app.models.assessment import Assessment
from app.models.assessment_remediation import AssessmentRemediation
from app.models.assessment_result import AssessmentResult


class AssessmentRemediationService:
    """Build deterministic review guidance from assessment results."""

    def create_remediation(
        self,
        assessment: Assessment,
        result: AssessmentResult,
    ) -> list[AssessmentRemediation]:
        if result.passed:
            return []

        incorrect_question_ids = set(
            result.incorrect_question_ids
        )

        return [
            AssessmentRemediation(
                question_id=question.id,
                prompt=question.prompt,
                explanation=question.explanation,
            )
            for question in assessment.questions
            if question.id in incorrect_question_ids
        ]
