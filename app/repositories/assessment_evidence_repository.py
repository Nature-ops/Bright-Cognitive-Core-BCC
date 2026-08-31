from abc import ABC, abstractmethod

from app.models.assessment_evidence import AssessmentEvidence


class AssessmentEvidenceRepository(ABC):
    """Long-term historical assessment evidence for learner intelligence."""

    @abstractmethod
    def record_attempt(self, evidence: AssessmentEvidence) -> None:
        """Append one completed assessment attempt."""

    @abstractmethod
    def list_attempts(self) -> list[AssessmentEvidence]:
        """Return assessment attempts in their recorded order."""
