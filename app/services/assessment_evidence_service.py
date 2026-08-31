import json
from pathlib import Path

from app.models.assessment_evidence import AssessmentEvidence


class AssessmentEvidenceService:
    """JSON persistence for append-only assessment evidence."""

    def __init__(self):
        self.evidence_file = Path("data/assessment_evidence.json")

        if not self.evidence_file.exists():
            self.evidence_file.write_text("[]", encoding="utf-8")

    def load(self) -> list[AssessmentEvidence]:
        try:
            data = json.loads(
                self.evidence_file.read_text(encoding="utf-8")
            )
        except FileNotFoundError:
            return []

        return [
            AssessmentEvidence.model_validate(item)
            for item in data
        ]

    def save(self, evidence_records: list[AssessmentEvidence]) -> None:
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

    def append(self, evidence: AssessmentEvidence) -> None:
        records = self.load()
        records.append(evidence)
        self.save(records)