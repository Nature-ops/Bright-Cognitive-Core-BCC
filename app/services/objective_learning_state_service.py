from app.models.assessment_evidence import AssessmentEvidence
from app.models.objective_learning_state import ObjectiveLearningState


class ObjectiveLearningStateService:
    """Interpret current objective state from ordered assessment evidence."""

    def current_learning_states(
        self,
        evidence_records: list[AssessmentEvidence],
    ) -> list[ObjectiveLearningState]:
        missed_attempt_counts: dict[tuple[str, str], int] = {}
        successful_counts_after_last_miss: dict[tuple[str, str], int] = {}

        for evidence in evidence_records:
            missed_objective_ids = set(
                evidence.learning_gap_objective_ids
            )

            for objective_id in dict.fromkeys(
                evidence.learning_gap_objective_ids
            ):
                key = (evidence.framework_id, objective_id)
                missed_attempt_counts[key] = (
                    missed_attempt_counts.get(key, 0) + 1
                )
                successful_counts_after_last_miss[key] = 0

            for objective_id in dict.fromkeys(
                evidence.successful_objective_ids
            ):
                if objective_id in missed_objective_ids:
                    continue

                key = (evidence.framework_id, objective_id)

                if key in missed_attempt_counts:
                    successful_counts_after_last_miss[key] = (
                        successful_counts_after_last_miss.get(key, 0) + 1
                    )

        learning_states = []

        for (framework_id, objective_id), missed_attempt_count in (
            missed_attempt_counts.items()
        ):
            if missed_attempt_count < 2:
                continue

            key = (framework_id, objective_id)
            successful_attempt_count = (
                successful_counts_after_last_miss.get(key, 0)
            )

            learning_states.append(
                ObjectiveLearningState(
                    framework_id=framework_id,
                    objective_id=objective_id,
                    state=(
                        "RECOVERY_EVIDENCE"
                        if successful_attempt_count > 0
                        else "REPEATED_GAP"
                    ),
                    historical_missed_attempt_count=missed_attempt_count,
                    successful_attempt_count_after_last_miss=(
                        successful_attempt_count
                    ),
                )
            )

        return learning_states
