from app.services.planning_engine import PlanningEngine
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryProgressService,
)


class MilestoneProgressionTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.framework_id = "aws-sa"
        self.progress_service = TemporaryProgressService()
        self.planner = PlanningEngine()
        self.planner.load_framework(
            "knowledge/cloud/frameworks/aws-sa.yaml"
        )

    def test_completing_iam_selects_ec2(self):
        progress = self.progress_service.get_progress(
            self.framework_id
        )
        progress.completed_milestones = ["aws-fundamentals"]
        self.progress_service.update_progress(progress)

        plan = self.planner.create_learning_plan_for_framework(
            self.framework_id
        )

        self.assertIsNotNone(plan)
        assert plan is not None
        self.assertEqual(plan.milestone.id, "iam")

        self.progress_service.complete_milestone(
            framework_id=self.framework_id,
            milestone_id="iam",
        )

        next_plan = self.planner.create_learning_plan_for_framework(
            self.framework_id
        )

        self.assertIsNotNone(next_plan)
        assert next_plan is not None
        self.assertEqual(next_plan.milestone.id, "ec2")


if __name__ == "__main__":
    import unittest

    unittest.main()
