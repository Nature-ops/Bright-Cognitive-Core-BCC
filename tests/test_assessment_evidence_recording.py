from app.models.assessment import Assessment
from app.models.assessment_evidence import AssessmentEvidence
from app.models.question import Question
from app.repositories.assessment_evidence_repository import (
    AssessmentEvidenceRepository,
)
from app.core.learning.session_controller import SessionController
from app.services.study_engine import StudyEngine
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryProgressService,
    TemporaryStudyProgressService,
)
from tests.test_utils import build_study_session, iam_passing_answers


class InMemoryAssessmentEvidenceRepository(
    AssessmentEvidenceRepository
):
    def __init__(self):
        self.attempts: list[AssessmentEvidence] = []

    def record_attempt(self, evidence: AssessmentEvidence) -> None:
        self.attempts.append(evidence.model_copy(deep=True))

    def list_attempts(self) -> list[AssessmentEvidence]:
        return [attempt.model_copy(deep=True) for attempt in self.attempts]


class AssessmentEvidenceRecordingTest(IsolatedProgressTestCase):
    def test_controller_injects_evidence_repository(self):
        framework_progress = TemporaryProgressService().get_progress(
            "aws-sa"
        )
        framework_progress.completed_milestones = ["aws-fundamentals"]
        TemporaryProgressService().update_progress(framework_progress)
        repository = InMemoryAssessmentEvidenceRepository()
        controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml",
            assessment_evidence_repository=repository,
        )

        controller.start()
        controller.submit_assessment(
            {
                "iam-q1": "Internet Access Manager",
                "iam-q2": "IAM Group",
                "iam-q3": "Maximum access",
            }
        )

        self.assertEqual(len(repository.list_attempts()), 1)
        self.assertFalse(repository.list_attempts()[0].passed)

    def test_attempts_are_retained_after_session_completion(self):
        session = build_study_session()
        repository = InMemoryAssessmentEvidenceRepository()
        engine = StudyEngine(assessment_evidence_repository=repository)
        engine.start_session(session)

        failed_result = engine.submit_assessment(
            {
                "iam-q1": "Internet Access Manager",
                "iam-q2": "IAM Group",
                "iam-q3": "Maximum access",
            }
        )

        while objective := engine.current_objective():
            engine.complete_objective(objective.id)

        while exercise := engine.current_exercise():
            engine.complete_exercise(exercise.id)

        passed_result = engine.submit_assessment(iam_passing_answers())

        self.assertFalse(failed_result.passed)
        self.assertTrue(passed_result.passed)
        self.assertTrue(TemporaryStudyProgressService().exists(session.id))
        self.assertTrue(engine.finish_session())
        self.assertFalse(TemporaryStudyProgressService().exists(session.id))
        self.assertEqual(
            [attempt.passed for attempt in repository.list_attempts()],
            [False, True],
        )
        self.assertEqual(
            repository.list_attempts()[0].incorrect_question_ids,
            ["iam-q1", "iam-q2", "iam-q3"],
        )
        self.assertEqual(
            repository.list_attempts()[0].learning_gap_objective_ids,
            ["iam-users", "iam-policies"],
        )

    def test_passing_imperfect_attempt_preserves_gap_evidence(self):
        session = build_study_session()
        session.assessment = Assessment(
            id="boundary-assessment",
            title="Boundary",
            passing_score=70,
            questions=[
                Question(
                    id=f"q{index}",
                    objective_id=(
                        "iam-users" if index < 9 else "iam-policies"
                    ),
                    prompt=f"Question {index}",
                    answer="Correct",
                )
                for index in range(10)
            ],
        )
        repository = InMemoryAssessmentEvidenceRepository()
        engine = StudyEngine(assessment_evidence_repository=repository)
        engine.start_session(session)

        result = engine.submit_assessment(
            {
                f"q{index}": "Correct" if index < 7 else "Wrong"
                for index in range(10)
            }
        )

        evidence = repository.list_attempts()[0]

        self.assertEqual(result.score, 70.0)
        self.assertTrue(result.passed)
        self.assertEqual(
            evidence.incorrect_question_ids,
            ["q7", "q8", "q9"],
        )
        self.assertEqual(
            evidence.learning_gap_objective_ids,
            ["iam-users", "iam-policies"],
        )
