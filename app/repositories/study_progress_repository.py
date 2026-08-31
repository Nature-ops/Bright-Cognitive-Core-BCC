from abc import ABC, abstractmethod

from app.models.study_progress import StudyProgress


class StudyProgressRepository(ABC):
    """Persistence required to resume and finalize study sessions."""

    @abstractmethod
    def load(self, session_id: str) -> StudyProgress | None:
        """Return persisted progress for a study session, if present."""

    @abstractmethod
    def save(self, progress: StudyProgress) -> None:
        """Persist the current state of a study session."""

    @abstractmethod
    def delete(self, session_id: str) -> None:
        """Remove progress for a successfully completed session."""
