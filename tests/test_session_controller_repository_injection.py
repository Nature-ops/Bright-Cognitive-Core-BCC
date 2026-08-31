from app.core.learning.session_controller import SessionController
from app.models.progress import Progress
from app.repositories.learning_progress_repository import (
    LearningProgressRepository,
)
from tests.persistence_fixtures import IsolatedProgressTestCase
from tests.test_utils import iam_passing_answers


class InMemoryLearningProgressRepository(
    LearningProgressRepository
):
    def __init__(self, progress: Progress):
        self.progress = progress

    def get_progress(self, framework_id: str) -> Progress:
        assert framework_id == self.progress.framework_id

        return self.progress

    def complete_milestone(
        self,
        framework_id: str,
        milestone_id: str,
    ) -> None:
        progress = self.get_progress(framework_id)

        if milestone_id not in progress.completed_milestones:
            progress.completed_milestones.append(milestone_id)

    def milestone_progress(
        self,
        framework_id: str,
        milestone_ids: list[str],
    ) -> float:
        progress = self.get_progress(framework_id)

        if not milestone_ids:
            return 100.0

        completed = sum(
            milestone_id in progress.completed_milestones
            for milestone_id in milestone_ids
        )

        return completed / len(milestone_ids) * 100


class SessionControllerRepositoryInjectionTest(
    IsolatedProgressTestCase
):
    def test_injected_repository_drives_planning_and_completion(self):
        repository = InMemoryLearningProgressRepository(
            Progress(
                framework_id="aws-sa",
                completed_milestones=["aws-fundamentals"],
            )
        )
        controller = SessionController(
            "knowledge/cloud/frameworks/aws-sa.yaml",
            repository,
        )

        session = controller.start()

        self.assertIsNotNone(session)
        assert session is not None
        self.assertEqual(session.learning_plan.milestone.id, "iam")

        while controller.current_objective() is not None:
            controller.complete_current_objective()

        while controller.current_exercise() is not None:
            controller.complete_current_exercise()

        result = controller.submit_assessment(iam_passing_answers())

        self.assertTrue(result.passed)

        next_session = controller.advance_to_next_milestone()

        self.assertIsNotNone(next_session)
        assert next_session is not None
        self.assertEqual(next_session.learning_plan.milestone.id, "ec2")
        self.assertEqual(
            repository.get_progress("aws-sa").completed_milestones,
            ["aws-fundamentals", "iam"],
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
