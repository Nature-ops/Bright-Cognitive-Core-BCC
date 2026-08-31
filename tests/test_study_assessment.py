import app.services.study_engine as study_engine_module
from tests.persistence_fixtures import IsolatedProgressTestCase
from tests.test_utils import (
    build_study_session,
    iam_passing_answers,
)


class StudyAssessmentTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.session = build_study_session()
        self.engine = study_engine_module.StudyEngine()
        self.engine.start_session(self.session)

    def test_failed_assessment_does_not_complete_progress(self):
        failed_result = self.engine.submit_assessment(
            {
                "iam-q1": "Internet Access Manager",
                "iam-q2": "IAM Group",
                "iam-q3": "Maximum access",
            }
        )

        self.assertFalse(failed_result.passed)
        self.assertIsNotNone(self.engine.progress)
        assert self.engine.progress is not None
        self.assertFalse(self.engine.progress.assessment_completed)

    def test_passing_assessment_completes_progress(self):
        passed_result = self.engine.submit_assessment(
            iam_passing_answers()
        )

        self.assertTrue(passed_result.passed)
        self.assertIsNotNone(self.engine.progress)
        assert self.engine.progress is not None
        self.assertTrue(self.engine.progress.assessment_completed)

if __name__ == "__main__":
    import unittest

    unittest.main()
