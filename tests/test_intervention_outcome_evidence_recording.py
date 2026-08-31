from datetime import UTC

from app.core.learning.session_controller import SessionController
from app.models.assessment_evidence import AssessmentEvidence
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from app.repositories.json_intervention_outcome_evidence_repository import (
    JsonInterventionOutcomeEvidenceRepository,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryAssessmentEvidenceService,
    TemporaryInterventionOutcomeEvidenceService,
)


def assessment_evidence(
    assessment_id: str,
    gaps: list[str] | None = None,
    successes: list[str] | None = None,
) -> AssessmentEvidence:
    return AssessmentEvidence(
        framework_id="aws-sa",
        milestone_id="iam",
        assessment_id=assessment_id,
        score=0.0,
        passed=False,
        learning_gap_objective_ids=gaps or [],
        successful_objective_ids=successes or [],
    )


class InterventionOutcomeEvidenceRecordingTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()
        self.assessment_repository = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        )
        self.outcome_repository = (
            JsonInterventionOutcomeEvidenceRepository(
                TemporaryInterventionOutcomeEvidenceService()
            )
        )
        self.controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml",
            assessment_evidence_repository=self.assessment_repository,
            intervention_outcome_evidence_repository=(
                self.outcome_repository
            ),
        )

    def test_controller_records_completed_reinforcement_outcome(self):
        self.assessment_repository.record_attempt(
            assessment_evidence("first", gaps=["iam-users"])
        )
        self.assessment_repository.record_attempt(
            assessment_evidence("second", gaps=["iam-users"])
        )
        intervention = self.controller.targeted_learning_interventions()[0]
        intervention_before = intervention.model_dump()
        states_before = [
            state.model_dump()
            for state in self.controller.current_learning_states()
        ]
        decisions_before = [
            decision.model_dump()
            for decision in self.controller.learning_decisions()
        ]
        assessment_history_before = [
            evidence.model_dump()
            for evidence in self.assessment_repository.list_attempts()
        ]

        outcome = self.controller.record_intervention_outcome(
            intervention,
            "COMPLETED",
        )

        self.assertEqual(outcome.framework_id, "aws-sa")
        self.assertEqual(outcome.objective_id, "iam-users")
        self.assertEqual(outcome.intervention_type, "REINFORCEMENT")
        self.assertEqual(outcome.required_activity, "PRACTICE")
        self.assertEqual(outcome.completion_status, "COMPLETED")
        self.assertEqual(outcome.source_action, "REINFORCE_OBJECTIVE")
        self.assertIs(outcome.recorded_at.tzinfo, UTC)
        self.assertEqual(self.controller.intervention_outcomes(), [outcome])
        self.assertEqual(intervention.model_dump(), intervention_before)
        self.assertEqual(
            [
                state.model_dump()
                for state in self.controller.current_learning_states()
            ],
            states_before,
        )
        self.assertEqual(
            [
                decision.model_dump()
                for decision in self.controller.learning_decisions()
            ],
            decisions_before,
        )
        self.assertEqual(
            [
                evidence.model_dump()
                for evidence in self.assessment_repository.list_attempts()
            ],
            assessment_history_before,
        )

    def test_identical_intervention_attempts_are_append_only(self):
        self.assessment_repository.record_attempt(
            assessment_evidence("first", gaps=["iam-users"])
        )
        self.assessment_repository.record_attempt(
            assessment_evidence("second", gaps=["iam-users"])
        )
        intervention = self.controller.targeted_learning_interventions()[0]

        self.controller.record_intervention_outcome(
            intervention,
            "NOT_COMPLETED",
        )
        self.controller.record_intervention_outcome(
            intervention,
            "COMPLETED",
        )

        self.assertEqual(
            [
                outcome.completion_status
                for outcome in self.controller.intervention_outcomes()
            ],
            ["NOT_COMPLETED", "COMPLETED"],
        )

    def test_controller_preserves_recovery_verification_identity(self):
        self.assessment_repository.record_attempt(
            assessment_evidence("first", gaps=["iam-users"])
        )
        self.assessment_repository.record_attempt(
            assessment_evidence("second", gaps=["iam-users"])
        )
        self.assessment_repository.record_attempt(
            assessment_evidence("third", successes=["iam-users"])
        )
        intervention = self.controller.targeted_learning_interventions()[0]

        outcome = self.controller.record_intervention_outcome(
            intervention,
            "COMPLETED",
        )

        self.assertEqual(outcome.intervention_type, "RECOVERY_VERIFICATION")
        self.assertEqual(outcome.required_activity, "ASSESSMENT")
        self.assertEqual(outcome.source_action, "VERIFY_RECOVERY")
