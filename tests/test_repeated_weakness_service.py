from app.core.learning.session_controller import SessionController
from app.models.assessment_evidence import AssessmentEvidence
from app.repositories.assessment_evidence_repository import (
    AssessmentEvidenceRepository,
)
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from app.services.repeated_weakness_service import RepeatedWeaknessService
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryAssessmentEvidenceService,
)


class InMemoryAssessmentEvidenceRepository(
    AssessmentEvidenceRepository
):
    def __init__(self, attempts: list[AssessmentEvidence] | None = None):
        self.attempts = attempts or []

    def record_attempt(self, evidence: AssessmentEvidence) -> None:
        self.attempts.append(evidence.model_copy(deep=True))

    def list_attempts(self) -> list[AssessmentEvidence]:
        return [attempt.model_copy(deep=True) for attempt in self.attempts]


def evidence(
    assessment_id: str,
    objective_ids: list[str],
    framework_id: str = "aws-sa",
    passed: bool = False,
) -> AssessmentEvidence:
    return AssessmentEvidence(
        framework_id=framework_id,
        milestone_id="iam",
        assessment_id=assessment_id,
        score=70.0 if passed else 0.0,
        passed=passed,
        learning_gap_objective_ids=objective_ids,
    )


class RepeatedWeaknessServiceTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()
        self.service = RepeatedWeaknessService()

    def test_one_missed_attempt_is_not_a_repeated_weakness(self):
        self.assertEqual(
            self.service.find_repeated_weaknesses(
                [evidence("iam-assessment", ["iam-users"])]
            ),
            [],
        )

    def test_counts_separate_attempts_not_questions(self):
        attempts = [
            evidence("iam-assessment", ["iam-users", "iam-users"]),
            evidence("iam-assessment", ["iam-users"]),
        ]

        self.assertEqual(
            [
                weakness.model_dump()
                for weakness in self.service.find_repeated_weaknesses(
                    attempts
                )
            ],
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "missed_attempt_count": 2,
                    "source_assessment_ids": [
                        "iam-assessment",
                        "iam-assessment",
                    ],
                }
            ],
        )

    def test_keeps_objectives_frameworks_and_order_separate(self):
        attempts = [
            evidence("first", ["iam-policies"]),
            evidence("second", ["iam-users"]),
            evidence("third", ["iam-policies"]),
            evidence("fourth", ["iam-users"]),
            evidence("other", ["iam-users"], framework_id="other"),
            evidence("other", ["iam-users"], framework_id="other"),
        ]

        self.assertEqual(
            [
                weakness.model_dump()
                for weakness in self.service.find_repeated_weaknesses(
                    attempts
                )
            ],
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-policies",
                    "missed_attempt_count": 2,
                    "source_assessment_ids": ["first", "third"],
                },
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "missed_attempt_count": 2,
                    "source_assessment_ids": ["second", "fourth"],
                },
                {
                    "framework_id": "other",
                    "objective_id": "iam-users",
                    "missed_attempt_count": 2,
                    "source_assessment_ids": ["other", "other"],
                },
            ],
        )

    def test_perfect_and_later_correct_attempts_do_not_clear_history(self):
        attempts = [
            evidence("first", ["iam-users"]),
            evidence("second", ["iam-users"], passed=True),
            evidence("third", [], passed=True),
        ]

        weaknesses = self.service.find_repeated_weaknesses(attempts)

        self.assertEqual(weaknesses[0].objective_id, "iam-users")
        self.assertEqual(weaknesses[0].missed_attempt_count, 2)

    def test_json_history_is_available_through_controller_query(self):
        repository = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        )
        repository.record_attempt(evidence("first", ["iam-users"]))
        repository.record_attempt(evidence("second", ["iam-users"]))
        reloaded_repository = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        )
        controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml",
            assessment_evidence_repository=reloaded_repository,
        )

        self.assertEqual(
            [
                weakness.model_dump()
                for weakness in controller.repeated_weaknesses()
            ],
            [
                {
                    "framework_id": "aws-sa",
                    "objective_id": "iam-users",
                    "missed_attempt_count": 2,
                    "source_assessment_ids": ["first", "second"],
                }
            ],
        )
