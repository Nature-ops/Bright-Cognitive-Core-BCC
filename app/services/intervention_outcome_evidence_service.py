import json
from pathlib import Path

from app.models.intervention_outcome_evidence import (
    InterventionOutcomeEvidence,
)


class InterventionOutcomeEvidenceService:
    """JSON persistence for append-only intervention outcome evidence."""

    def __init__(self):
        self.evidence_file = Path("data/intervention_outcome_evidence.json")

    def load(self) -> list[InterventionOutcomeEvidence]:
        try:
            data = json.loads(
                self.evidence_file.read_text(encoding="utf-8")
            )
        except FileNotFoundError:
            return []

        return [
            InterventionOutcomeEvidence.model_validate(item)
            for item in data
        ]

    def save(
        self,
        evidence_records: list[InterventionOutcomeEvidence],
    ) -> None:
        self.evidence_file.write_text(
            json.dumps(
                [
                    evidence.model_dump(mode="json")
                    for evidence in evidence_records
                ],
                indent=2,
            ),
            encoding="utf-8",
        )

    def append(self, evidence: InterventionOutcomeEvidence) -> None:
        records = self.load()
        records.append(evidence)
        self.save(records)
