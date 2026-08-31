from app.models.assessment_evidence import AssessmentEvidence
from app.repositories.assessment_evidence_repository import (
    AssessmentEvidenceRepository,
)
from app.services.assessment_evidence_service import (
    AssessmentEvidenceService,
)


class JsonAssessmentEvidenceRepository(AssessmentEvidenceRepository):
    """JSON-backed long-term assessment evidence."""

    def __init__(
        self,
        assessment_evidence_service: AssessmentEvidenceService | None = None,
    ):
        self.assessment_evidence_service = (
            assessment_evidence_service
            or AssessmentEvidenceService()
        )

    def record_attempt(self, evidence: AssessmentEvidence) -> None:
        self.assessment_evidence_service.append(evidence)

    def list_attempts(self) -> list[AssessmentEvidence]:
        return self.assessment_evidence_service.load()
