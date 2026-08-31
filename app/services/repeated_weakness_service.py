from app.models.assessment_evidence import AssessmentEvidence
from app.models.repeated_weakness import RepeatedWeakness


class RepeatedWeaknessService:
    """Derive repeated objective gaps from historical assessment attempts."""

    def find_repeated_weaknesses(
        self,
        evidence_records: list[AssessmentEvidence],
    ) -> list[RepeatedWeakness]:
        missed_attempt_counts: dict[tuple[str, str], int] = {}
        source_assessment_ids: dict[tuple[str, str], list[str]] = {}

        for evidence in evidence_records:
            objective_ids = dict.fromkeys(
                evidence.learning_gap_objective_ids
            )

            for objective_id in objective_ids:
                key = (evidence.framework_id, objective_id)
                missed_attempt_counts[key] = (
                    missed_attempt_counts.get(key, 0) + 1
                )
                source_assessment_ids.setdefault(key, []).append(
                    evidence.assessment_id
                )

        return [
            RepeatedWeakness(
                framework_id=framework_id,
                objective_id=objective_id,
                missed_attempt_count=missed_attempt_counts[
                    (framework_id, objective_id)
                ],
                source_assessment_ids=source_assessment_ids[
                    (framework_id, objective_id)
                ],
            )
            for framework_id, objective_id in missed_attempt_counts
            if missed_attempt_counts[(framework_id, objective_id)] >= 2
        ]
