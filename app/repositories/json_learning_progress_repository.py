from app.models.progress import Progress
from app.repositories.learning_progress_repository import (
    LearningProgressRepository,
)
from app.services.progress_service import ProgressService


class JsonLearningProgressRepository(LearningProgressRepository):
    """JSON-backed framework progress using the existing ProgressService."""

    def __init__(self, progress_service: ProgressService | None = None):
        self.progress_service = progress_service or ProgressService()

    def get_progress(self, framework_id: str) -> Progress:
        return self.progress_service.get_progress(framework_id)

    def complete_milestone(
        self,
        framework_id: str,
        milestone_id: str,
    ) -> None:
        self.progress_service.complete_milestone(
            framework_id,
            milestone_id,
        )

    def milestone_progress(
        self,
        framework_id: str,
        milestone_ids: list[str],
    ) -> float:
        return self.progress_service.milestone_progress(
            framework_id,
            milestone_ids,
        )
