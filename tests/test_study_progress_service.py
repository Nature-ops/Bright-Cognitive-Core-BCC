from app.models.study_progress import StudyProgress
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryStudyProgressService,
)


class StudyProgressServiceTest(IsolatedProgressTestCase):
    def test_save_load_and_delete_progress(self):
        service = TemporaryStudyProgressService()
        progress = StudyProgress(
            session_id="test-session",
            completed_objectives=["iam-users"],
            completed_exercises=["iam-lab"],
            assessment_completed=True,
        )

        service.save(progress)

        self.assertTrue(service.exists(progress.session_id))

        reloaded_progress = TemporaryStudyProgressService().load(
            progress.session_id
        )

        self.assertEqual(reloaded_progress, progress)

        service.delete(progress.session_id)

        self.assertFalse(service.exists(progress.session_id))


if __name__ == "__main__":
    import unittest

    unittest.main()
