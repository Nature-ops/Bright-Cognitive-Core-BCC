from abc import ABC, abstractmethod

from app.models.intervention_outcome_evidence import (
    InterventionOutcomeEvidence,
)


class InterventionOutcomeEvidenceRepository(ABC):
    """Append-only historical evidence of intervention activity outcomes."""

    @abstractmethod
    def record_outcome(
        self,
        evidence: InterventionOutcomeEvidence,
    ) -> None:
        """Append one intervention outcome record."""

    @abstractmethod
    def list_outcomes(self) -> list[InterventionOutcomeEvidence]:
        """Return outcome records in their recorded order."""
