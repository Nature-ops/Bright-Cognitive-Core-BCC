from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import app.services.planning_engine as planning_engine_module
import app.services.study_engine as study_engine_module
from app.services.progress_service import ProgressService
from app.services.study_progress_service import StudyProgressService
from tests.test_utils import build_study_session


class TemporaryProgressService(ProgressService):
    progress_file_path: Path

    def __init__(self):
        self.progress_file = self.progress_file_path

        if not self.progress_file.exists():
            self.progress_file.write_text("[]", encoding="utf-8")


class TemporaryStudyProgressService(StudyProgressService):
    progress_directory_path: Path

    def __init__(self):
        self.progress_directory = self.progress_directory_path
        self.progress_directory.mkdir(parents=True, exist_ok=True)


class MilestoneCompletionTest(TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        temporary_path = Path(self.temporary_directory.name)

        TemporaryProgressService.progress_file_path = (
            temporary_path / "progress.json"
        )
        TemporaryStudyProgressService.progress_directory_path = (
            temporary_path / "study_progress"
        )

        patches = [
            patch.object(
                planning_engine_module,
                "ProgressService",
                TemporaryProgressService,
            ),
            patch.object(
                study_engine_module,
                "ProgressService",
                TemporaryProgressService,
            ),
            patch.object(
                study_engine_module,
                "StudyProgressService",
                TemporaryStudyProgressService,
            ),
        ]

        for service_patch in patches:
            service_patch.start()
            self.addCleanup(service_patch.stop)

        self.session = build_study_session()
        self.framework_progress = TemporaryProgressService()

    def test_finishing_completed_session_records_milestone(self):
        framework_id = self.session.learning_plan.framework.id
        milestone_id = self.session.learning_plan.milestone.id

        progress = self.framework_progress.get_progress(framework_id)
        self.assertNotIn(milestone_id, progress.completed_milestones)

        engine = study_engine_module.StudyEngine()
        engine.start_session(self.session)

        while objective := engine.current_objective():
            engine.complete_objective(objective.id)

        while exercise := engine.current_exercise():
            engine.complete_exercise(exercise.id)

        assessment = self.session.assessment
        self.assertIsNotNone(assessment)

        answers = {
            question.id: question.answer
            for question in assessment.questions
        }
        result = engine.submit_assessment(answers)

        self.assertTrue(result.passed)
        self.assertTrue(engine.is_completed())
        self.assertTrue(engine.finish_session())

        stored_progress = self.framework_progress.get_progress(framework_id)

        self.assertEqual(
            stored_progress.completed_milestones.count(milestone_id),
            1,
        )
        self.assertFalse(
            engine.progress_service.exists(self.session.id)
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
