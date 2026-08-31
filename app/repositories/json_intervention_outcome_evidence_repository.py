from app.models.intervention_outcome_evidence import (
    InterventionOutcomeEvidence,
)
from app.repositories.intervention_outcome_evidence_repository import (
    InterventionOutcomeEvidenceRepository,
)
from app.services.intervention_outcome_evidence_service import (
    InterventionOutcomeEvidenceService,
)


class JsonInterventionOutcomeEvidenceRepository(
    InterventionOutcomeEvidenceRepository
):
    """JSON-backed long-term intervention outcome evidence."""

    def __init__(
        self,
        intervention_outcome_evidence_service: (
            InterventionOutcomeEvidenceService | None
        ) = None,
    ):
        self.intervention_outcome_evidence_service = (
            intervention_outcome_evidence_service
            or InterventionOutcomeEvidenceService()
        )

    def record_outcome(
        self,
        evidence: InterventionOutcomeEvidence,
    ) -> None:
        self.intervention_outcome_evidence_service.append(evidence)

    def list_outcomes(self) -> list[InterventionOutcomeEvidence]:
        return self.intervention_outcome_evidence_service.load()
