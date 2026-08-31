from app.core.learning.session_controller import SessionController
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryProgressService,
)


class FrameworkCompletionTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml"
        )

        progress = TemporaryProgressService().get_progress(
            "aws-sa"
        )
        progress.completed_milestones = [
            "aws-fundamentals",
            "iam",
            "ec2",
            "s3",
        ]
        TemporaryProgressService().update_progress(progress)

    def test_completing_final_milestone_completes_framework(self):
        session = self.controller.start()

        self.assertIsNotNone(session)
        assert session is not None
        self.assertEqual(session.learning_plan.milestone.id, "vpc")

        while self.controller.current_objective() is not None:
            self.controller.complete_current_objective()

        while self.controller.current_exercise() is not None:
            self.controller.complete_current_exercise()

        self.assertTrue(self.controller.session_completed())
        self.assertIsNone(self.controller.advance_to_next_milestone())

        completed_milestones = self.controller.completed_milestones()

        self.assertEqual(completed_milestones.count("vpc"), 1)
        self.assertEqual(
            completed_milestones,
            ["aws-fundamentals", "iam", "ec2", "s3", "vpc"],
        )
        self.assertIsNone(
            self.controller.planner.create_learning_plan_for_framework(
                "aws-sa"
            )
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
