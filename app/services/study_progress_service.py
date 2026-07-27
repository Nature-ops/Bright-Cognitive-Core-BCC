from json import JSONDecodeError
from pathlib import Path

from app.models.study_progress import StudyProgress


class StudyProgressService:

    def __init__(self):

        self.progress_directory = Path("data/study_progress")

        self.progress_directory.mkdir(
            parents=True,
            exist_ok=True,
        )


    def _progress_file(
        self,
        session_id: str,
    ) -> Path:

            return self.progress_directory / f"{session_id}.json"    


    def save(
        self,
        progress: StudyProgress,
    ) -> None:

        self._progress_file(
            progress.session_id
        ).write_text(
            progress.model_dump_json(indent=2),
            encoding="utf-8",
        )


    def load(
        self,
            session_id: str,
    ) -> StudyProgress | None:

        file = self._progress_file(session_id)

        if not file.exists():
            return None

        try:
            return StudyProgress.model_validate_json(
                    file.read_text(encoding="utf-8")
                )

        except JSONDecodeError:
            return None


    def exists(
        self,
        session_id: str,
    ) -> bool:

        return self._progress_file(
            session_id
        ).exists()   


    def delete(
        self,
        session_id: str,
    ) -> None:

        file = self._progress_file(session_id)

        if file.exists():
            file.unlink() 

    