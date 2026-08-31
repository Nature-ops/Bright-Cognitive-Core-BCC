from app.services.planning_engine import PlanningEngine
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryProgressService,
)


class DependencyOrderingTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.framework_id = "aws-sa"
        self.progress_service = TemporaryProgressService()
        self.planner = PlanningEngine()
        self.planner.load_framework(
            "knowledge/cloud/frameworks/aws-sa.yaml"
        )

    def test_next_plan_does_not_bypass_uncompleted_prerequisite(self):
        progress = self.progress_service.get_progress(
            self.framework_id
        )
        progress.completed_milestones = [
            "aws-fundamentals",
            "iam",
            "s3",
        ]
        self.progress_service.update_progress(progress)

        plan = self.planner.create_learning_plan_for_framework(
            self.framework_id
        )

        self.assertIsNotNone(plan)
        assert plan is not None
        self.assertEqual(plan.milestone.id, "ec2")


if __name__ == "__main__":
    import unittest

    unittest.main()
