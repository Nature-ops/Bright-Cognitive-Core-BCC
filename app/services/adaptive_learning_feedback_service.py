from app.models.adaptive_learning_feedback import AdaptiveLearningFeedback
from app.models.intervention_outcome_evidence import (
    InterventionOutcomeEvidence,
)
from app.models.targeted_learning_intervention import (
    TargetedLearningIntervention,
)


class AdaptiveLearningFeedbackService:
    """Interpret the latest matching outcome for each intervention."""

    def create_adaptive_feedback(
        self,
        interventions: list[TargetedLearningIntervention],
        outcomes: list[InterventionOutcomeEvidence],
    ) -> list[AdaptiveLearningFeedback]:
        feedback_items = []

        for intervention in interventions:
            matching_outcomes = [
                outcome
                for outcome in outcomes
                if (
                    outcome.framework_id == intervention.framework_id
                    and outcome.objective_id == intervention.objective_id
                    and outcome.intervention_type
                    == intervention.intervention_type
                    and outcome.required_activity
                    == intervention.required_activity
                    and outcome.source_action == intervention.source_action
                )
            ]

            if not matching_outcomes:
                continue

            outcome = matching_outcomes[-1]
            feedback_state, reason = self._feedback_for(
                intervention,
                outcome,
            )

            feedback_items.append(
                AdaptiveLearningFeedback(
                    framework_id=intervention.framework_id,
                    objective_id=intervention.objective_id,
                    source_intervention_type=(
                        intervention.intervention_type
                    ),
                    source_completion_status=outcome.completion_status,
                    feedback_state=feedback_state,
                    reason=reason,
                )
            )

        return feedback_items

    def _feedback_for(
        self,
        intervention: TargetedLearningIntervention,
        outcome: InterventionOutcomeEvidence,
    ) -> tuple[str, str]:
        if outcome.completion_status == "NOT_COMPLETED":
            if intervention.intervention_type == "REINFORCEMENT":
                reason = (
                    "The targeted practice was not completed and remains "
                    "unresolved."
                )
            else:
                reason = (
                    "The recovery verification was not completed and "
                    "remains unresolved."
                )

            return "REPEAT_INTERVENTION", reason

        if intervention.intervention_type == "REINFORCEMENT":
            return (
                "READY_FOR_VERIFICATION",
                "Targeted practice was completed and the objective should "
                "now be verified.",
            )

        return (
            "AWAITING_ASSESSMENT_EVIDENCE",
            "The verification activity was completed; assessment evidence "
            "is required before changing learner state.",
        )
