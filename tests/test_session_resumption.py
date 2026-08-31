import app.services.study_engine as study_engine_module
from app.models.study_progress import StudyProgress
from app.repositories.study_progress_repository import (
    StudyProgressRepository,
)
from tests.persistence_fixtures import IsolatedProgressTestCase
from tests.test_utils import (
    build_study_session,
    iam_passing_answers,
)


class InMemoryStudyProgressRepository(StudyProgressRepository):
    def __init__(self):
        self.records: dict[str, StudyProgress] = {}

    def load(self, session_id: str) -> StudyProgress | None:
        progress = self.records.get(session_id)

        if progress is None:
            return None

        return progress.model_copy(deep=True)

    def save(self, progress: StudyProgress) -> None:
        self.records[progress.session_id] = progress.model_copy(deep=True)

    def delete(self, session_id: str) -> None:
        self.records.pop(session_id, None)


class SessionResumptionTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.session = build_study_session()

    def test_restarts_with_persisted_session_progress(self):
        repository = InMemoryStudyProgressRepository()

        first_engine = study_engine_module.StudyEngine(
            study_progress_repository=repository,
        )
        first_engine.start_session(self.session)

        first_objective = first_engine.current_objective()
        self.assertIsNotNone(first_objective)
        assert first_objective is not None
        first_engine.complete_objective(first_objective.id)

        exercise = first_engine.current_exercise()
        self.assertIsNotNone(exercise)
        assert exercise is not None
        first_engine.complete_exercise(exercise.id)

        result = first_engine.submit_assessment(
            iam_passing_answers()
        )

        self.assertTrue(result.passed)
        self.assertIn(self.session.id, repository.records)

        resumed_engine = study_engine_module.StudyEngine(
            study_progress_repository=repository,
        )
        resumed_engine.start_session(self.session)

        self.assertIsNotNone(resumed_engine.progress)
        assert resumed_engine.progress is not None
        self.assertEqual(
            resumed_engine.progress.completed_objectives,
            [first_objective.id],
        )
        self.assertEqual(
            resumed_engine.progress.completed_exercises,
            [exercise.id],
        )
        self.assertTrue(resumed_engine.progress.assessment_completed)

        resumed_objective = resumed_engine.current_objective()

        self.assertIsNotNone(resumed_objective)
        assert resumed_objective is not None
        self.assertNotEqual(resumed_objective.id, first_objective.id)
        self.assertIsNone(resumed_engine.current_exercise())


if __name__ == "__main__":
    import unittest

    unittest.main()
