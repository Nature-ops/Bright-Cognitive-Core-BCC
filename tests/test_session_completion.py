import app.services.study_engine as study_engine_module
from tests.persistence_fixtures import IsolatedProgressTestCase
from tests.test_utils import (
    build_study_session,
    iam_passing_answers,
)


class SessionCompletionTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.session = build_study_session()
        self.engine = study_engine_module.StudyEngine()
        self.engine.start_session(self.session)

    def test_session_completion_requires_all_requirements(self):
        while objective := self.engine.current_objective():
            self.engine.complete_objective(objective.id)

        self.assertFalse(self.engine.is_completed())
        self.assertFalse(self.engine.finish_session())

        while exercise := self.engine.current_exercise():
            self.engine.complete_exercise(exercise.id)

        self.assertFalse(self.engine.is_completed())
        self.assertFalse(self.engine.finish_session())

        failed_result = self.engine.submit_assessment(
            {
                "iam-q1": "Internet Access Manager",
                "iam-q2": "IAM Group",
                "iam-q3": "Maximum access",
            }
        )

        self.assertFalse(failed_result.passed)
        self.assertFalse(self.engine.is_completed())
        self.assertFalse(self.engine.finish_session())

        passed_result = self.engine.submit_assessment(
            iam_passing_answers()
        )

        self.assertTrue(passed_result.passed)
        self.assertTrue(self.engine.is_completed())
        self.assertTrue(self.engine.finish_session())

if __name__ == "__main__":
    import unittest

    unittest.main()
