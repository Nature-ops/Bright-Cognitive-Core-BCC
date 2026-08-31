from app.core.learning.session_controller import SessionController
from app.models.assessment_evidence import AssessmentEvidence
from app.models.objective_learning_state import ObjectiveLearningState
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from app.services.learning_decision_service import LearningDecisionService
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryAssessmentEvidenceService,
)


def learning_state(
    objective_id: str,
    state: str,
    framework_id: str = "aws-sa",
) -> ObjectiveLearningState:
    return ObjectiveLearningState(
        framework_id=framework_id,
        objective_id=objective_id,
        state=state,
        historical_missed_attempt_count=2,
        successful_attempt_count_after_last_miss=(
            1 if state == "RECOVERY_EVIDENCE" else 0
        ),
    )


def evidence(
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


class LearningDecisionServiceTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()
        self.service = LearningDecisionService()

    def test_repeated_gap_produces_reinforcement_decision(self):
        decision = self.service.create_learning_decisions(
            [learning_state("iam-users", "REPEATED_GAP")]
        )[0]

        self.assertEqual(decision.framework_id, "aws-sa")
        self.assertEqual(decision.objective_id, "iam-users")
        self.assertEqual(decision.source_state, "REPEATED_GAP")
        self.assertEqual(decision.action, "REINFORCE_OBJECTIVE")
        self.assertEqual(
            decision.reason,
            "Repeated assessment gaps require targeted reinforcement.",
        )

    def test_recovery_evidence_produces_verification_decision(self):
        decision = self.service.create_learning_decisions(
            [learning_state("iam-users", "RECOVERY_EVIDENCE")]
        )[0]

        self.assertEqual(decision.source_state, "RECOVERY_EVIDENCE")
        self.assertEqual(decision.action, "VERIFY_RECOVERY")
        self.assertEqual(
            decision.reason,
            "Recent successful evidence should be verified before "
            "considering the objective recovered.",
        )

    def test_preserves_input_order_frameworks_and_state_objects(self):
        learning_states = [
            learning_state("iam-users", "REPEATED_GAP"),
            learning_state(
                "ec2-instances",
                "RECOVERY_EVIDENCE",
                framework_id="aws-developer",
            ),
            learning_state("iam-policies", "REPEATED_GAP"),
        ]
        original_states = [state.model_dump() for state in learning_states]

        decisions = self.service.create_learning_decisions(learning_states)

        self.assertEqual(len(decisions), 3)
        self.assertEqual(
            [
                (decision.framework_id, decision.objective_id)
                for decision in decisions
            ],
            [
                ("aws-sa", "iam-users"),
                ("aws-developer", "ec2-instances"),
                ("aws-sa", "iam-policies"),
            ],
        )
        self.assertEqual(
            [state.model_dump() for state in learning_states],
            original_states,
        )

    def test_empty_states_produce_no_decisions(self):
        self.assertEqual(self.service.create_learning_decisions([]), [])

    def test_controller_uses_current_learning_state_history(self):
        repository = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        )
        repository.record_attempt(evidence("first", gaps=["iam-users"]))
        repository.record_attempt(evidence("second", gaps=["iam-users"]))
        controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml",
            assessment_evidence_repository=(
                JsonAssessmentEvidenceRepository(
                    TemporaryAssessmentEvidenceService()
                )
            ),
        )

        repeated_gap_decision = controller.learning_decisions()[0]

        self.assertEqual(
            repeated_gap_decision.action,
            "REINFORCE_OBJECTIVE",
        )

        repository.record_attempt(
            evidence("third", successes=["iam-users"])
        )

        recovery_decision = controller.learning_decisions()[0]

        self.assertEqual(recovery_decision.action, "VERIFY_RECOVERY")
