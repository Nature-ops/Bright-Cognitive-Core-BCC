from datetime import UTC, datetime
from json import JSONDecodeError

from app.models.intervention_outcome_evidence import (
    InterventionOutcomeEvidence,
)
from app.repositories.json_intervention_outcome_evidence_repository import (
    JsonInterventionOutcomeEvidenceRepository,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryInterventionOutcomeEvidenceService,
)


def outcome(
    completion_status: str,
    framework_id: str = "aws-sa",
) -> InterventionOutcomeEvidence:
    return InterventionOutcomeEvidence(
        framework_id=framework_id,
        objective_id="iam-users",
        intervention_type="REINFORCEMENT",
        required_activity="PRACTICE",
        completion_status=completion_status,
        source_action="REINFORCE_OBJECTIVE",
        recorded_at=datetime(2026, 1, 1, tzinfo=UTC),
    )


class JsonInterventionOutcomeEvidenceRepositoryTest(
    IsolatedProgressTestCase
):
    def test_missing_storage_is_empty_and_outcomes_persist_in_order(self):
        service = TemporaryInterventionOutcomeEvidenceService()
        repository = JsonInterventionOutcomeEvidenceRepository(
            service
        )
        completed_outcome = outcome("COMPLETED")
        not_completed_outcome = outcome(
            "NOT_COMPLETED",
            framework_id="aws-developer",
        )

        self.assertFalse(service.evidence_file.exists())
        self.assertEqual(repository.list_outcomes(), [])
        self.assertFalse(service.evidence_file.exists())

        repository.record_outcome(completed_outcome)
        repository.record_outcome(not_completed_outcome)

        reloaded_outcomes = JsonInterventionOutcomeEvidenceRepository(
            TemporaryInterventionOutcomeEvidenceService()
        ).list_outcomes()

        self.assertEqual(
            reloaded_outcomes,
            [completed_outcome, not_completed_outcome],
        )

    def test_corrupt_storage_raises_instead_of_erasing_history(self):
        service = TemporaryInterventionOutcomeEvidenceService()
        service.evidence_file.write_text(
            "{invalid json",
            encoding="utf-8",
        )

        repository = JsonInterventionOutcomeEvidenceRepository(service)

        with self.assertRaises(JSONDecodeError):
            repository.list_outcomes()
