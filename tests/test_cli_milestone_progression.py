from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from app.cli.cli import BrightCLI
from app.core.learning.session_controller import SessionController
from tests.persistence_fixtures import IsolatedProgressTestCase
from tests.persistence_fixtures import TemporaryProgressService


class CLIMilestoneProgressionTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml"
        )

        progress = TemporaryProgressService().get_progress(
            "aws-sa"
        )
        progress.completed_milestones = ["aws-fundamentals"]
        TemporaryProgressService().update_progress(progress)

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
            TemporaryProgressService()
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
