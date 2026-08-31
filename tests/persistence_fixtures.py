from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import app.services.planning_engine as planning_engine_module
import app.services.study_engine as study_engine_module
from app.repositories.json_learning_progress_repository import (
    JsonLearningProgressRepository,
)
from app.repositories.json_study_progress_repository import (
    JsonStudyProgressRepository,
)
from app.services.progress_service import ProgressService
from app.services.study_progress_service import StudyProgressService


class TemporaryProgressService(ProgressService):
    progress_file_path: Path

    def __init__(self):
        self.progress_file = self.progress_file_path

        if not self.progress_file.exists():
            self.progress_file.write_text("[]", encoding="utf-8")


class TemporaryStudyProgressService(StudyProgressService):
    progress_directory_path: Path

    def __init__(self):
        self.progress_directory = self.progress_directory_path
        self.progress_directory.mkdir(parents=True, exist_ok=True)


class TemporaryLearningProgressRepository(
    JsonLearningProgressRepository
):
    def __init__(self):
        super().__init__(TemporaryProgressService())


class TemporaryStudyProgressRepository(
    JsonStudyProgressRepository
):
    def __init__(self):
        super().__init__(TemporaryStudyProgressService())


class IsolatedProgressTestCase(TestCase):
    def setUp(self):
        super().setUp()

        temporary_directory = TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)

        temporary_path = Path(temporary_directory.name)

        TemporaryProgressService.progress_file_path = (
            temporary_path / "progress.json"
        )
        TemporaryStudyProgressService.progress_directory_path = (
            temporary_path / "study_progress"
        )

        patches = [
            patch.object(
                planning_engine_module,
                "JsonLearningProgressRepository",
                TemporaryLearningProgressRepository,
            ),
            patch.object(
                study_engine_module,
                "JsonLearningProgressRepository",
                TemporaryLearningProgressRepository,
            ),
            patch.object(
                study_engine_module,
                "JsonStudyProgressRepository",
                TemporaryStudyProgressRepository,
            ),
        ]

        for service_patch in patches:
            service_patch.start()
            self.addCleanup(service_patch.stop)
