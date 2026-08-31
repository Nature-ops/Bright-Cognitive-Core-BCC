from app.models.assessment_evidence import AssessmentEvidence
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryAssessmentEvidenceService,
)
from json import JSONDecodeError


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
        )
        passed_attempt = AssessmentEvidence(
            framework_id="aws-sa",
            milestone_id="iam",
            assessment_id="iam-assessment",
            score=100.0,
            passed=True,
        )

        self.assertEqual(repository.list_attempts(), [])

        repository.record_attempt(failed_attempt)
        repository.record_attempt(passed_attempt)

        reloaded_attempts = JsonAssessmentEvidenceRepository(
            TemporaryAssessmentEvidenceService()
        ).list_attempts()

        self.assertEqual(reloaded_attempts, [failed_attempt, passed_attempt])


    def test_corrupt_storage_raises_instead_of_erasing_history(self):
        service = TemporaryAssessmentEvidenceService()
        service.evidence_file.write_text(
            "{invalid json",
            encoding="utf-8",
        )

        repository = JsonAssessmentEvidenceRepository(service)

        with self.assertRaises(JSONDecodeError):
            repository.list_attempts()
