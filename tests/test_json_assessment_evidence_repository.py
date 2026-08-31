import json
from json import JSONDecodeError

from app.models.assessment_evidence import AssessmentEvidence
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryAssessmentEvidenceService,
)


class JsonAssessmentEvidenceRepositoryTest(IsolatedProgressTestCase):
    def test_missing_storage_is_empty_and_attempts_persist_in_order(self):
        repository = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        )
        failed_attempt = AssessmentEvidence(
            framework_id="aws-sa",
            milestone_id="iam",
            assessment_id="iam-assessment",
            score=0.0,
            passed=False,
            incorrect_question_ids=["iam-q1"],
            learning_gap_objective_ids=["iam-users"],
            assessed_objective_ids=["iam-users"],
        )
        passed_attempt = AssessmentEvidence(
            framework_id="aws-sa",
            milestone_id="iam",
            assessment_id="iam-assessment",
            score=100.0,
            passed=True,
            assessed_objective_ids=["iam-users"],
            successful_objective_ids=["iam-users"],
        )

        self.assertEqual(repository.list_attempts(), [])

        repository.record_attempt(failed_attempt)
        repository.record_attempt(passed_attempt)

        reloaded_attempts = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        ).list_attempts()

        self.assertEqual(reloaded_attempts, [failed_attempt, passed_attempt])

    def test_legacy_records_load_without_positive_objective_evidence(self):
        service = TemporaryAssessmentEvidenceService()
        service.evidence_file.write_text(
            json.dumps(
                [
                    {
                        "framework_id": "aws-sa",
                        "milestone_id": "iam",
                        "assessment_id": "iam-assessment",
                        "score": 0.0,
                        "passed": False,
                        "learning_gap_objective_ids": ["iam-users"],
                        "recorded_at": "2026-01-01T00:00:00Z",
                    }
                ]
            ),
            encoding="utf-8",
        )

        evidence = JsonAssessmentEvidenceRepository(service).list_attempts()[0]

        self.assertEqual(evidence.assessed_objective_ids, [])
        self.assertEqual(evidence.successful_objective_ids, [])

    def test_corrupt_storage_raises_instead_of_erasing_history(self):
        service = TemporaryAssessmentEvidenceService()
        service.evidence_file.write_text(
            "{invalid json",
            encoding="utf-8",
        )

        repository = JsonAssessmentEvidenceRepository(service)

        with self.assertRaises(JSONDecodeError):
            repository.list_attempts()
