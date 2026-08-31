from app.models.study_progress import StudyProgress
from app.repositories.study_progress_repository import (
    StudyProgressRepository,
)
from app.services.study_progress_service import StudyProgressService


class JsonStudyProgressRepository(StudyProgressRepository):
    """JSON-backed study-session progress using StudyProgressService."""

    def __init__(
        self,
        study_progress_service: StudyProgressService | None = None,
    ):
        self.study_progress_service = (
            study_progress_service
            or StudyProgressService()
        )

    def load(self, session_id: str) -> StudyProgress | None:
        return self.study_progress_service.load(session_id)

    def save(self, progress: StudyProgress) -> None:
        self.study_progress_service.save(progress)

    def delete(self, session_id: str) -> None:
        self.study_progress_service.delete(session_id)
