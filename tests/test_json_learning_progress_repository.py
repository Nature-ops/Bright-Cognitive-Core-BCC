from app.repositories.json_learning_progress_repository import (
    JsonLearningProgressRepository,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryProgressService,
)


class JsonLearningProgressRepositoryTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.repository = JsonLearningProgressRepository(
            TemporaryProgressService()
        )

    def test_framework_progress_operations_delegate_to_json_service(self):
        framework_id = "aws-sa"

        progress = self.repository.get_progress(framework_id)

        self.assertEqual(progress.framework_id, framework_id)
        self.assertEqual(progress.completed_milestones, [])

        self.repository.complete_milestone(
            framework_id,
            "aws-fundamentals",
        )
        self.repository.complete_milestone(
            framework_id,
            "aws-fundamentals",
        )

        reloaded_progress = JsonLearningProgressRepository(
            TemporaryProgressService()
        ).get_progress(framework_id)

        self.assertEqual(
            reloaded_progress.completed_milestones,
            ["aws-fundamentals"],
        )
        self.assertEqual(
            self.repository.milestone_progress(
                framework_id,
                ["aws-fundamentals", "iam"],
            ),
            50.0,
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
