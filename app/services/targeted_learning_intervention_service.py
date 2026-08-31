from app.models.learning_decision import LearningDecision
from app.models.targeted_learning_intervention import (
    TargetedLearningIntervention,
)


class TargetedLearningInterventionService:
    """Translate deterministic learning decisions into intervention specs."""

    def create_targeted_interventions(
        self,
        learning_decisions: list[LearningDecision],
    ) -> list[TargetedLearningIntervention]:
        interventions = []

        for decision in learning_decisions:
            if decision.action == "REINFORCE_OBJECTIVE":
                intervention_type = "REINFORCEMENT"
                required_activity = "PRACTICE"
                reason = (
                    "Provide targeted practice for the objective before "
                    "further progression."
                )
            else:
                intervention_type = "RECOVERY_VERIFICATION"
                required_activity = "ASSESSMENT"
                reason = (
                    "Verify that recent recovery evidence is stable through "
                    "reassessment."
                )

            interventions.append(
                TargetedLearningIntervention(
                    framework_id=decision.framework_id,
                    objective_id=decision.objective_id,
                    intervention_type=intervention_type,
                    reason=reason,
                    source_action=decision.action,
                    required_activity=required_activity,
                )
            )

        return interventions
