from app.models.assessment import Assessment
from app.models.assessment_result import AssessmentResult
from app.models.objective_assessment_evidence import (
    ObjectiveAssessmentEvidence,
)


class ObjectiveAssessmentEvidenceService:
    """Derive explicit objective assessment and success facts."""

    def create_evidence(
        self,
        assessment: Assessment,
        result: AssessmentResult,
    ) -> ObjectiveAssessmentEvidence:
        question_ids_by_objective: dict[str, list[str]] = {}

        for question in assessment.questions:
            if question.objective_id is None:
                continue

            question_ids_by_objective.setdefault(
                question.objective_id,
                [],
            ).append(question.id)

        incorrect_question_ids = set(result.incorrect_question_ids)

        return ObjectiveAssessmentEvidence(
            assessed_objective_ids=list(question_ids_by_objective),
            successful_objective_ids=[
                objective_id
                for objective_id, question_ids in (
                    question_ids_by_objective.items()
                )
                if not any(
                    question_id in incorrect_question_ids
                    for question_id in question_ids
                )
            ],
        )
