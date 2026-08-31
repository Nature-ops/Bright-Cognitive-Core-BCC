from app.models.study_progress import StudyProgress
from app.repositories.json_study_progress_repository import (
    JsonStudyProgressRepository,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryStudyProgressService,
)


class JsonStudyProgressRepositoryTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.repository = JsonStudyProgressRepository(
            TemporaryStudyProgressService()
        )

    def test_progress_survives_reloading_the_json_adapter(self):
        progress = StudyProgress(
            session_id="test-session",
            completed_objectives=["iam-users"],
            assessment_completed=True,
        )

        self.repository.save(progress)

        reloaded_progress = JsonStudyProgressRepository(
            TemporaryStudyProgressService()
        ).load(progress.session_id)

        self.assertEqual(reloaded_progress, progress)

        self.repository.delete(progress.session_id)

        self.assertIsNone(self.repository.load(progress.session_id))


if __name__ == "__main__":
    import unittest

    unittest.main()
