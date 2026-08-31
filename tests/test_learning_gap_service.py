from unittest import TestCase

from app.models.assessment import Assessment
from app.models.question import Question
from app.services.assessment_service import AssessmentService
from app.services.learning_gap_service import LearningGapService


def build_assessment() -> Assessment:
    return Assessment(
        id="assessment",
        title="Assessment",
        passing_score=70,
        questions=[
            Question(
                id="q1",
                objective_id="iam-users",
                prompt="Question 1",
                answer="Correct",
            ),
            Question(
                id="q2",
                objective_id="iam-users",
                prompt="Question 2",
                answer="Correct",
            ),
            Question(
                id="q3",
                objective_id="iam-policies",
                prompt="Question 3",
                answer="Correct",
            ),
            Question(
                id="q4",
                objective_id="iam-policies",
                prompt="Question 4",
                answer="Correct",
            ),
        ],
    )


class LearningGapServiceTest(TestCase):
    def setUp(self):
        self.assessment_service = AssessmentService()
        self.learning_gap_service = LearningGapService()

    def test_groups_incorrect_questions_by_objective(self):
        assessment = build_assessment()
        result = self.assessment_service.evaluate(
            assessment,
            {
                "q1": "Wrong",
                "q2": "Wrong",
                "q3": "Wrong",
                "q4": "Correct",
            },
        )

        gaps = self.learning_gap_service.create_learning_gaps(
            assessment,
            result,
        )

        self.assertEqual(
            [
                (
                    gap.objective_id,
                    gap.reason,
                    gap.source_question_ids,
                )
                for gap in gaps
            ],
            [
                (
                    "iam-users",
                    "Incorrect assessment responses for this objective.",
                    ["q1", "q2"],
                ),
                (
                    "iam-policies",
                    "Incorrect assessment responses for this objective.",
                    ["q3"],
                ),
            ],
        )

    def test_perfect_assessment_has_no_learning_gaps(self):
        assessment = build_assessment()
        result = self.assessment_service.evaluate(
            assessment,
            {question.id: "Correct" for question in assessment.questions},
        )

        self.assertEqual(
            self.learning_gap_service.create_learning_gaps(
                assessment,
                result,
            ),
            [],
        )

    def test_passing_imperfect_assessment_still_has_learning_gaps(self):
        questions = [
            Question(
                id=f"q{index}",
                objective_id=(
                    "iam-users" if index < 9 else "iam-policies"
                ),
                prompt=f"Question {index}",
                answer="Correct",
            )
            for index in range(10)
        ]
        assessment = Assessment(
            id="boundary",
            title="Boundary",
            passing_score=70,
            questions=questions,
        )
        result = self.assessment_service.evaluate(
            assessment,
            {
                question.id: "Correct" if index < 7 else "Wrong"
                for index, question in enumerate(questions)
            },
        )

        gaps = self.learning_gap_service.create_learning_gaps(
            assessment,
            result,
        )

        self.assertEqual(result.score, 70.0)
        self.assertTrue(result.passed)
        self.assertEqual(
            [
                (gap.objective_id, gap.source_question_ids)
                for gap in gaps
            ],
            [
                ("iam-users", ["q7", "q8"]),
                ("iam-policies", ["q9"]),
            ],
        )
