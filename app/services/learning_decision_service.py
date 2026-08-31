from app.models.learning_decision import LearningDecision
from app.models.objective_learning_state import ObjectiveLearningState


class LearningDecisionService:
    """Convert current objective states into deterministic learning actions."""

    def create_learning_decisions(
        self,
        learning_states: list[ObjectiveLearningState],
    ) -> list[LearningDecision]:
        decisions = []

        for learning_state in learning_states:
            if learning_state.state == "REPEATED_GAP":
                action = "REINFORCE_OBJECTIVE"
                reason = (
                    "Repeated assessment gaps require targeted "
                    "reinforcement."
                )
            else:
                action = "VERIFY_RECOVERY"
                reason = (
                    "Recent successful evidence should be verified before "
                    "considering the objective recovered."
                )

            decisions.append(
                LearningDecision(
                    framework_id=learning_state.framework_id,
                    objective_id=learning_state.objective_id,
                    action=action,
                    reason=reason,
                    source_state=learning_state.state,
                )
            )

        return decisions
