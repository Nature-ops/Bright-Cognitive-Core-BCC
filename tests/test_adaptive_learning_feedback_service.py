from app.core.learning.session_controller import SessionController
from app.models.assessment_evidence import AssessmentEvidence
from app.models.intervention_outcome_evidence import (
    InterventionOutcomeEvidence,
)
from app.models.targeted_learning_intervention import (
    TargetedLearningIntervention,
)
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from app.repositories.json_intervention_outcome_evidence_repository import (
    JsonInterventionOutcomeEvidenceRepository,
)
from app.services.adaptive_learning_feedback_service import (
    AdaptiveLearningFeedbackService,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryAssessmentEvidenceService,
    TemporaryInterventionOutcomeEvidenceService,
)


def intervention(
    objective_id: str,
    intervention_type: str,
    framework_id: str = "aws-sa",
) -> TargetedLearningIntervention:
    is_reinforcement = intervention_type == "REINFORCEMENT"

    return TargetedLearningIntervention(
        framework_id=framework_id,
        objective_id=objective_id,
        intervention_type=intervention_type,
        reason="Existing intervention reason.",
        source_action=(
            "REINFORCE_OBJECTIVE"
            if is_reinforcement
            else "VERIFY_RECOVERY"
        ),
        required_activity="PRACTICE" if is_reinforcement else "ASSESSMENT",
    )


def outcome(
    source_intervention: TargetedLearningIntervention,
    completion_status: str,
) -> InterventionOutcomeEvidence:
    return InterventionOutcomeEvidence(
        framework_id=source_intervention.framework_id,
        objective_id=source_intervention.objective_id,
        intervention_type=source_intervention.intervention_type,
        required_activity=source_intervention.required_activity,
        completion_status=completion_status,
        source_action=source_intervention.source_action,
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


class AdaptiveLearningFeedbackServiceTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()
        self.service = AdaptiveLearningFeedbackService()

    def test_reinforcement_outcomes_map_to_repeat_or_verification(self):
        source = intervention("iam-users", "REINFORCEMENT")

        not_completed = self.service.create_adaptive_feedback(
            [source],
            [outcome(source, "NOT_COMPLETED")],
        )[0]
        completed = self.service.create_adaptive_feedback(
            [source],
            [outcome(source, "COMPLETED")],
        )[0]

        self.assertEqual(not_completed.feedback_state, "REPEAT_INTERVENTION")
        self.assertEqual(
            not_completed.source_intervention_type,
            "REINFORCEMENT",
        )
        self.assertEqual(
            not_completed.source_completion_status,
            "NOT_COMPLETED",
        )
        self.assertEqual(
            not_completed.reason,
            "The targeted practice was not completed and remains "
            "unresolved.",
        )
        self.assertEqual(completed.feedback_state, "READY_FOR_VERIFICATION")
        self.assertEqual(completed.framework_id, "aws-sa")
        self.assertEqual(completed.objective_id, "iam-users")
        self.assertEqual(completed.source_completion_status, "COMPLETED")
        self.assertEqual(
            completed.reason,
            "Targeted practice was completed and the objective should now "
            "be verified.",
        )

    def test_recovery_outcomes_map_to_repeat_or_assessment_evidence(self):
        source = intervention("iam-users", "RECOVERY_VERIFICATION")

        not_completed = self.service.create_adaptive_feedback(
            [source],
            [outcome(source, "NOT_COMPLETED")],
        )[0]
        completed = self.service.create_adaptive_feedback(
            [source],
            [outcome(source, "COMPLETED")],
        )[0]

        self.assertEqual(not_completed.feedback_state, "REPEAT_INTERVENTION")
        self.assertEqual(
            not_completed.reason,
            "The recovery verification was not completed and remains "
            "unresolved.",
        )
        self.assertEqual(
            completed.feedback_state,
            "AWAITING_ASSESSMENT_EVIDENCE",
        )
        self.assertEqual(
            completed.reason,
            "The verification activity was completed; assessment evidence "
            "is required before changing learner state.",
        )

    def test_latest_matching_outcome_wins_and_unrelated_outcomes_are_ignored(self):
        source = intervention("iam-users", "REINFORCEMENT")
        unrelated = intervention(
            "iam-policies",
            "REINFORCEMENT",
        )

        feedback = self.service.create_adaptive_feedback(
            [source],
            [
                outcome(source, "COMPLETED"),
                outcome(unrelated, "NOT_COMPLETED"),
                outcome(source, "NOT_COMPLETED"),
            ],
        )

        self.assertEqual(len(feedback), 1)
        self.assertEqual(feedback[0].source_completion_status, "NOT_COMPLETED")
        self.assertEqual(feedback[0].feedback_state, "REPEAT_INTERVENTION")

        feedback = self.service.create_adaptive_feedback(
            [source],
            [
                outcome(source, "NOT_COMPLETED"),
                outcome(source, "COMPLETED"),
            ],
        )

        self.assertEqual(feedback[0].source_completion_status, "COMPLETED")
        self.assertEqual(
            feedback[0].feedback_state,
            "READY_FOR_VERIFICATION",
        )

    def test_preserves_intervention_order_frameworks_and_inputs(self):
        interventions = [
            intervention("iam-users", "REINFORCEMENT"),
            intervention(
                "ec2-instances",
                "RECOVERY_VERIFICATION",
                framework_id="aws-developer",
            ),
            intervention("iam-policies", "REINFORCEMENT"),
        ]
        outcomes = [
            outcome(interventions[0], "COMPLETED"),
            outcome(interventions[1], "NOT_COMPLETED"),
            outcome(interventions[2], "COMPLETED"),
        ]
        original_interventions = [item.model_dump() for item in interventions]
        original_outcomes = [item.model_dump() for item in outcomes]

        feedback = self.service.create_adaptive_feedback(
            interventions,
            outcomes,
        )

        self.assertEqual(
            [
                (item.framework_id, item.objective_id)
                for item in feedback
            ],
            [
                ("aws-sa", "iam-users"),
                ("aws-developer", "ec2-instances"),
                ("aws-sa", "iam-policies"),
            ],
        )
        self.assertEqual(
            [item.model_dump() for item in interventions],
            original_interventions,
        )
        self.assertEqual(
            [item.model_dump() for item in outcomes],
            original_outcomes,
        )

    def test_no_matching_outcome_produces_no_feedback(self):
        source = intervention("iam-users", "REINFORCEMENT")

        self.assertEqual(
            self.service.create_adaptive_feedback([source], []),
            [],
        )

    def test_controller_feedback_does_not_change_repeated_gap_state(self):
        assessment_repository = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        )
        outcome_repository = JsonInterventionOutcomeEvidenceRepository(
            TemporaryInterventionOutcomeEvidenceService()
        )
        controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml",
            assessment_evidence_repository=assessment_repository,
            intervention_outcome_evidence_repository=outcome_repository,
        )
        assessment_repository.record_attempt(
            assessment_evidence("first", gaps=["iam-users"])
        )
        assessment_repository.record_attempt(
            assessment_evidence("second", gaps=["iam-users"])
        )
        intervention_specification = (
            controller.targeted_learning_interventions()[0]
        )

        controller.record_intervention_outcome(
            intervention_specification,
            "COMPLETED",
        )

        feedback = controller.adaptive_learning_feedback()[0]

        self.assertEqual(feedback.feedback_state, "READY_FOR_VERIFICATION")
        self.assertEqual(
            controller.current_learning_states()[0].state,
            "REPEATED_GAP",
        )

    def test_controller_feedback_does_not_change_recovery_evidence_state(self):
        assessment_repository = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        )
        outcome_repository = JsonInterventionOutcomeEvidenceRepository(
            TemporaryInterventionOutcomeEvidenceService()
        )
        controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml",
            assessment_evidence_repository=assessment_repository,
            intervention_outcome_evidence_repository=outcome_repository,
        )
        assessment_repository.record_attempt(
            assessment_evidence("first", gaps=["iam-users"])
        )
        assessment_repository.record_attempt(
            assessment_evidence("second", gaps=["iam-users"])
        )
        assessment_repository.record_attempt(
            assessment_evidence("third", successes=["iam-users"])
        )
        intervention_specification = (
            controller.targeted_learning_interventions()[0]
        )

        controller.record_intervention_outcome(
            intervention_specification,
            "COMPLETED",
        )

        feedback = controller.adaptive_learning_feedback()[0]

        self.assertEqual(
            feedback.feedback_state,
            "AWAITING_ASSESSMENT_EVIDENCE",
        )
        self.assertEqual(
            controller.current_learning_states()[0].state,
            "RECOVERY_EVIDENCE",
        )
