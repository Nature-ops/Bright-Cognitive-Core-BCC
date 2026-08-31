from app.core.learning.session_controller import SessionController
from app.models.assessment_evidence import AssessmentEvidence
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from app.services.objective_learning_state_service import (
    ObjectiveLearningStateService,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryAssessmentEvidenceService,
)


def evidence(
    assessment_id: str,
    gaps: list[str] | None = None,
    successes: list[str] | None = None,
    framework_id: str = "aws-sa",
    passed: bool = False,
) -> AssessmentEvidence:
    return AssessmentEvidence(
        framework_id=framework_id,
        milestone_id="iam",
        assessment_id=assessment_id,
        score=70.0 if passed else 0.0,
        passed=passed,
        learning_gap_objective_ids=gaps or [],
        successful_objective_ids=successes or [],
    )


class ObjectiveLearningStateServiceTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()
        self.service = ObjectiveLearningStateService()

    def states(self, attempts: list[AssessmentEvidence]):
        return [
            state.model_dump()
            for state in self.service.current_learning_states(attempts)
        ]

    def test_one_miss_does_not_create_a_current_repeated_state(self):
        self.assertEqual(self.states([evidence("first", ["iam-users"])]), [])

    def test_chronology_distinguishes_repeated_gap_and_recovery_evidence(
        self,
    ):
        misses = [
            evidence("first", ["iam-users"]),
            evidence("second", ["iam-users"]),
        ]
        self.assertEqual(
            self.states(misses),
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "state": "REPEATED_GAP",
                    "historical_missed_attempt_count": 2,
                    "successful_attempt_count_after_last_miss": 0,
                }
            ],
        )
        self.assertEqual(
            self.states(
                misses + [
                    evidence(
                        "third",
                        successes=["iam-users"],
                        passed=True,
                    )
                ]
            ),
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "state": "RECOVERY_EVIDENCE",
                    "historical_missed_attempt_count": 2,
                    "successful_attempt_count_after_last_miss": 1,
                }
            ],
        )
        self.assertEqual(
            self.states(
                misses + [
                    evidence("third", successes=["iam-users"]),
                    evidence("fourth", ["iam-users"]),
                ]
            ),
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "state": "REPEATED_GAP",
                    "historical_missed_attempt_count": 3,
                    "successful_attempt_count_after_last_miss": 0,
                }
            ],
        )

    def test_multiple_successes_and_legacy_records_do_not_fabricate_mastery_or_recovery(
        self,
    ):
        misses = [
            evidence("first", ["iam-users"]),
            evidence("second", ["iam-users"]),
        ]
        self.assertEqual(
            self.states(
                misses + [
                    evidence("third", successes=["iam-users"]),
                    evidence("fourth", successes=["iam-users"]),
                ]
            ),
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "state": "RECOVERY_EVIDENCE",
                    "historical_missed_attempt_count": 2,
                    "successful_attempt_count_after_last_miss": 2,
                }
            ],
        )
        self.assertEqual(
            self.states(misses + [evidence("legacy-empty")]),
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "state": "REPEATED_GAP",
                    "historical_missed_attempt_count": 2,
                    "successful_attempt_count_after_last_miss": 0,
                }
            ],
        )

    def test_frameworks_order_duplicates_and_passing_imperfect_evidence_are_handled_independently(
        self,
    ):
        attempts = [
            evidence("first", ["iam-policies", "iam-policies"]),
            evidence("second", ["iam-users"]),
            evidence("third", ["iam-policies"]),
            evidence("fourth", ["iam-users"]),
            evidence(
                "fifth",
                ["iam-policies"],
                successes=["iam-users"],
                passed=True,
            ),
            evidence("other-first", ["iam-users"], framework_id="other"),
            evidence("other-second", ["iam-users"], framework_id="other"),
        ]

        self.assertEqual(
            self.states(attempts),
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-policies",
                    "state": "REPEATED_GAP",
                    "historical_missed_attempt_count": 3,
                    "successful_attempt_count_after_last_miss": 0,
                },
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "state": "RECOVERY_EVIDENCE",
                    "historical_missed_attempt_count": 2,
                    "successful_attempt_count_after_last_miss": 1,
                },
                {
                    "framework_id": "other",
                    "objective_id": "iam-users",
                    "state": "REPEATED_GAP",
                    "historical_missed_attempt_count": 2,
                    "successful_attempt_count_after_last_miss": 0,
                },
            ],
        )

    def test_reloaded_json_history_is_available_through_controller_query(self):
        repository = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        )
        repository.record_attempt(evidence("first", ["iam-users"]))
        repository.record_attempt(evidence("second", ["iam-users"]))
        repository.record_attempt(
            evidence("third", successes=["iam-users"], passed=True)
        )
        controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml",
            assessment_evidence_repository=(
                JsonAssessmentEvidenceRepository(
                    TemporaryAssessmentEvidenceService()
                )
            ),
        )

        self.assertEqual(
            [
                state.model_dump()
                for state in controller.current_learning_states()
            ],
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "state": "RECOVERY_EVIDENCE",
                    "historical_missed_attempt_count": 2,
                    "successful_attempt_count_after_last_miss": 1,
                }
            ],
        )
