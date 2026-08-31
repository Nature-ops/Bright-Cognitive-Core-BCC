from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryProgressService,
)


class ProgressServiceTest(IsolatedProgressTestCase):
    def test_completed_milestone_persists_without_duplication(self):
        service = TemporaryProgressService()
        framework_id = "aws-sa"

        progress = service.get_progress(framework_id)

        self.assertEqual(progress.framework_id, framework_id)
        self.assertEqual(progress.completed_milestones, [])

        service.complete_milestone(
            framework_id,
            "aws-fundamentals",
        )
        service.complete_milestone(
            framework_id,
            "aws-fundamentals",
        )

        reloaded_progress = TemporaryProgressService().get_progress(
            framework_id
        )

        self.assertEqual(
            reloaded_progress.completed_milestones,
            ["aws-fundamentals"],
        )
        self.assertEqual(
            service.milestone_progress(
                framework_id,
                ["aws-fundamentals", "iam"],
            ),
            50.0,
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
