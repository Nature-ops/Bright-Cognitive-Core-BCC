from abc import ABC, abstractmethod

from app.models.progress import Progress


class LearningProgressRepository(ABC):
    """Framework-progress persistence required by learning engines."""

    @abstractmethod
    def get_progress(self, framework_id: str) -> Progress:
        """Return progress for a framework."""

    @abstractmethod
    def complete_milestone(
        self,
        framework_id: str,
        milestone_id: str,
    ) -> None:
        """Record a completed framework milestone."""

    @abstractmethod
    def milestone_progress(
        self,
        framework_id: str,
        milestone_ids: list[str],
    ) -> float:
        """Return the percentage of framework milestones completed."""
