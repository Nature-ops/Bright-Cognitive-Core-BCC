from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import app.services.planning_engine as planning_engine_module
import app.services.study_engine as study_engine_module
from app.cli.cli import BrightCLI
from app.core.learning.session_controller import SessionController
from app.services.progress_service import ProgressService
from app.services.study_progress_service import StudyProgressService


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


class CLIMilestoneProgressionTest(TestCase):
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

        self.controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml"
        )

        progress = self.controller.planner.progress.get_progress(
            "aws-sa"
        )
        progress.completed_milestones = ["aws-fundamentals"]
        self.controller.planner.progress.update_progress(progress)

    def test_passing_iam_advances_cli_to_ec2_without_restart(self):
        cli = BrightCLI(self.controller)
        output = StringIO()

        inputs = [
            "1", "",
            "1", "",
            "1", "",
            "1", "1", "2", "2",
            "7",
        ]

        with patch.object(
            self.controller,
            "start",
            wraps=self.controller.start,
        ) as start_session:
            with patch("builtins.input", side_effect=inputs):
                with redirect_stdout(output):
                    cli.run()

        rendered_output = output.getvalue()
        completed_milestones = (
            self.controller.planner.progress
            .get_progress("aws-sa")
            .completed_milestones
        )

        self.assertIn(
            "1. Identity and Access Management",
            rendered_output,
        )
        self.assertIn("2. IAM Role", rendered_output)
        self.assertIn("Correct: 3 / 3", rendered_output)
        self.assertIn("Score: 100%", rendered_output)
        self.assertIn("Status: PASSED", rendered_output)
        self.assertIn("Milestone completed!", rendered_output)
        self.assertIn("Amazon EC2", rendered_output)
        self.assertLess(
            rendered_output.index("Milestone completed!"),
            rendered_output.rindex("Amazon EC2"),
        )
        self.assertEqual(rendered_output.count("Current Milestone"), 2)
        self.assertEqual(start_session.call_count, 1)
        self.assertIsNotNone(self.controller.study_engine.session)
        self.assertEqual(
            self.controller.study_engine.session.learning_plan.milestone.id,
            "ec2",
        )
        self.assertEqual(completed_milestones.count("iam"), 1)
        self.assertFalse(self.controller._session_finished)


if __name__ == "__main__":
    import unittest

    unittest.main()
