from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import app.services.planning_engine as planning_engine_module
import app.services.study_engine as study_engine_module
import app.core.learning.session_controller as session_controller_module
from app.repositories.json_learning_progress_repository import (
    JsonLearningProgressRepository,
)
from app.repositories.json_study_progress_repository import (
    JsonStudyProgressRepository,
)
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from app.repositories.json_intervention_outcome_evidence_repository import (
    JsonInterventionOutcomeEvidenceRepository,
)
from app.services.assessment_evidence_service import (
    AssessmentEvidenceService,
)
from app.services.intervention_outcome_evidence_service import (
    InterventionOutcomeEvidenceService,
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


class TemporaryAssessmentEvidenceService(AssessmentEvidenceService):
    evidence_file_path: Path

    def __init__(self):
        self.evidence_file = self.evidence_file_path

        if not self.evidence_file.exists():
            self.evidence_file.write_text("[]", encoding="utf-8")


class TemporaryInterventionOutcomeEvidenceService(
    InterventionOutcomeEvidenceService
):
    evidence_file_path: Path

    def __init__(self):
        self.evidence_file = self.evidence_file_path


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


class TemporaryAssessmentEvidenceRepository(
    JsonAssessmentEvidenceRepository
):
    def __init__(self):
        super().__init__(TemporaryAssessmentEvidenceService())


class TemporaryInterventionOutcomeEvidenceRepository(
    JsonInterventionOutcomeEvidenceRepository
):
    def __init__(self):
        super().__init__(TemporaryInterventionOutcomeEvidenceService())


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
        TemporaryAssessmentEvidenceService.evidence_file_path = (
            temporary_path / "assessment_evidence.json"
        )
        TemporaryInterventionOutcomeEvidenceService.evidence_file_path = (
            temporary_path / "intervention_outcome_evidence.json"
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
            patch.object(
                study_engine_module,
                "JsonAssessmentEvidenceRepository",
                TemporaryAssessmentEvidenceRepository,
            ),
            patch.object(
                session_controller_module,
                "JsonAssessmentEvidenceRepository",
                TemporaryAssessmentEvidenceRepository,
            ),
            patch.object(
                session_controller_module,
                "JsonInterventionOutcomeEvidenceRepository",
                TemporaryInterventionOutcomeEvidenceRepository,
            ),
        ]

        for service_patch in patches:
            service_patch.start()
            self.addCleanup(service_patch.stop)
