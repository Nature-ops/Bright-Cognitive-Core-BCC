import app.services.study_engine as study_engine_module
from tests.persistence_fixtures import (
    IsolatedProgressTestCase,
    TemporaryProgressService,
)
from tests.test_utils import build_study_session


class MilestoneCompletionTest(IsolatedProgressTestCase):
    def setUp(self):
        super().setUp()

        self.session = build_study_session()
        self.framework_progress = TemporaryProgressService()

    def test_finishing_completed_session_records_milestone(self):
        framework_id = self.session.learning_plan.framework.id
        milestone_id = self.session.learning_plan.milestone.id

        progress = self.framework_progress.get_progress(framework_id)
        self.assertNotIn(milestone_id, progress.completed_milestones)

        engine = study_engine_module.StudyEngine()
        engine.start_session(self.session)

        while objective := engine.current_objective():
            engine.complete_objective(objective.id)

        while exercise := engine.current_exercise():
            engine.complete_exercise(exercise.id)

        assessment = self.session.assessment
        self.assertIsNotNone(assessment)

        answers = {
            question.id: question.answer
            for question in assessment.questions
        }
        result = engine.submit_assessment(answers)

        self.assertTrue(result.passed)
        self.assertTrue(engine.is_completed())
        self.assertTrue(engine.finish_session())

        stored_progress = self.framework_progress.get_progress(framework_id)

        self.assertEqual(
            stored_progress.completed_milestones.count(milestone_id),
            1,
        )
        self.assertFalse(
            engine.progress_service.exists(self.session.id)
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
