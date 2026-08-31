from app.models.assessment import Assessment
from app.models.assessment_result import AssessmentResult
from app.models.learning_gap import LearningGap


class LearningGapService:
    """Derive objective-level gaps from explicit assessment mappings."""

    def create_learning_gaps(
        self,
        assessment: Assessment,
        result: AssessmentResult,
    ) -> list[LearningGap]:
        incorrect_question_ids = set(
            result.incorrect_question_ids
        )
        question_ids_by_objective: dict[str, list[str]] = {}

        for question in assessment.questions:
            if (
                question.id not in incorrect_question_ids
                or question.objective_id is None
            ):
                continue

            question_ids_by_objective.setdefault(
                question.objective_id,
                [],
            ).append(question.id)

        return [
            LearningGap(
                objective_id=objective_id,
                reason=(
                    "Incorrect assessment responses for this objective."
                ),
                source_question_ids=question_ids,
            )
            for objective_id, question_ids in (
                question_ids_by_objective.items()
            )
        ]
