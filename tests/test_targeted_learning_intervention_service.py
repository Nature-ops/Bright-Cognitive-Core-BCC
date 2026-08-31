from app.core.learning.session_controller import SessionController
from app.models.assessment_evidence import AssessmentEvidence
from app.models.learning_decision import LearningDecision
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from app.services.targeted_learning_intervention_service import (
    TargetedLearningInterventionService,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryAssessmentEvidenceService,
)


def decision(
    objective_id: str,
    action: str,
    framework_id: str = "aws-sa",
) -> LearningDecision:
    return LearningDecision(
        framework_id=framework_id,
        objective_id=objective_id,
        action=action,
        reason="Existing decision reason.",
        source_state=(
            "REPEATED_GAP"
            if action == "REINFORCE_OBJECTIVE"
            else "RECOVERY_EVIDENCE"
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


class TargetedLearningInterventionServiceTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()
        self.service = TargetedLearningInterventionService()

    def test_reinforcement_decision_produces_practice_intervention(self):
        intervention = self.service.create_targeted_interventions(
            [decision("iam-users", "REINFORCE_OBJECTIVE")]
        )[0]

        self.assertEqual(intervention.framework_id, "aws-sa")
        self.assertEqual(intervention.objective_id, "iam-users")
        self.assertEqual(intervention.source_action, "REINFORCE_OBJECTIVE")
        self.assertEqual(intervention.intervention_type, "REINFORCEMENT")
        self.assertEqual(intervention.required_activity, "PRACTICE")
        self.assertEqual(
            intervention.reason,
            "Provide targeted practice for the objective before "
            "further progression.",
        )

    def test_recovery_decision_produces_assessment_intervention(self):
        intervention = self.service.create_targeted_interventions(
            [decision("iam-users", "VERIFY_RECOVERY")]
        )[0]

        self.assertEqual(intervention.source_action, "VERIFY_RECOVERY")
        self.assertEqual(
            intervention.intervention_type,
            "RECOVERY_VERIFICATION",
        )
        self.assertEqual(intervention.required_activity, "ASSESSMENT")
        self.assertEqual(
            intervention.reason,
            "Verify that recent recovery evidence is stable through "
            "reassessment.",
        )

    def test_preserves_order_frameworks_and_decision_objects(self):
        decisions = [
            decision("iam-users", "REINFORCE_OBJECTIVE"),
            decision(
                "ec2-instances",
                "VERIFY_RECOVERY",
                framework_id="aws-developer",
            ),
            decision("iam-policies", "REINFORCE_OBJECTIVE"),
        ]
        original_decisions = [item.model_dump() for item in decisions]

        interventions = self.service.create_targeted_interventions(decisions)

        self.assertEqual(len(interventions), 3)
        self.assertEqual(
            [
                (item.framework_id, item.objective_id)
                for item in interventions
            ],
            [
                ("aws-sa", "iam-users"),
                ("aws-developer", "ec2-instances"),
                ("aws-sa", "iam-policies"),
            ],
        )
        self.assertEqual(
            [item.model_dump() for item in decisions],
            original_decisions,
        )

    def test_empty_decisions_produce_no_interventions(self):
        self.assertEqual(self.service.create_targeted_interventions([]), [])

    def test_controller_derives_interventions_from_evidence_history(self):
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

        reinforcement = controller.targeted_learning_interventions()[0]

        self.assertEqual(reinforcement.intervention_type, "REINFORCEMENT")
        self.assertEqual(reinforcement.required_activity, "PRACTICE")

        repository.record_attempt(
            evidence("third", successes=["iam-users"])
        )

        verification = controller.targeted_learning_interventions()[0]

        self.assertEqual(
            verification.intervention_type,
            "RECOVERY_VERIFICATION",
        )
        self.assertEqual(verification.required_activity, "ASSESSMENT")
