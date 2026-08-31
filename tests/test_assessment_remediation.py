from unittest import TestCase

from app.models.assessment import Assessment
from app.models.question import Question
from app.services.assessment_remediation_service import (
    AssessmentRemediationService,
)
from app.services.assessment_service import AssessmentService


def build_assessment() -> Assessment:
    return Assessment(
        id="assessment",
        title="Assessment",
        passing_score=70,
        questions=[
            Question(
                id="q1",
                prompt="What is identity management?",
                answer="Identity and Access Management",
                explanation="Identity management controls access.",
            ),
            Question(
                id="q2",
                prompt="Which identity is assumable?",
                answer="IAM Role",
                explanation="IAM roles can be assumed.",
            ),
            Question(
                id="q3",
                prompt="Which permission principle applies?",
                answer="Least privilege",
                explanation="Grant only required permissions.",
            ),
        ],
    )


class AssessmentRemediationTest(TestCase):
    def setUp(self):
        self.assessment = build_assessment()
        self.assessment_service = AssessmentService()
        self.remediation_service = AssessmentRemediationService()

    def test_incorrect_answers_are_recorded_and_remediated(self):
        result = self.assessment_service.evaluate(
            self.assessment,
            {
                "q1": "  identity and access management  ",
                "q2": "IAM Group",
                "q3": "Maximum access",
            },
        )

        remediation = self.remediation_service.create_remediation(
            self.assessment,
            result,
        )

        self.assertEqual(result.correct_answers, 1)
        self.assertEqual(result.incorrect_question_ids, ["q2", "q3"])
        self.assertFalse(result.passed)
        self.assertEqual(
            [(item.question_id, item.prompt, item.explanation)
             for item in remediation],
            [
                (
                    "q2",
                    "Which identity is assumable?",
                    "IAM roles can be assumed.",
                ),
                (
                    "q3",
                    "Which permission principle applies?",
                    "Grant only required permissions.",
                ),
            ],
        )

    def test_passing_result_has_no_remediation(self):
        result = self.assessment_service.evaluate(
            self.assessment,
            {
                "q1": "Identity and Access Management",
                "q2": "IAM Role",
                "q3": "Least privilege",
            },
        )

        remediation = self.remediation_service.create_remediation(
            self.assessment,
            result,
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.incorrect_question_ids, [])
        self.assertEqual(remediation, [])

    def test_passing_score_boundary_preserves_scoring_without_remediation(self):
        questions = [
            Question(
                id=f"q{index}",
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
        answers = {
            question.id: "Correct" if index < 7 else "Wrong"
            for index, question in enumerate(questions)
        }

        result = self.assessment_service.evaluate(assessment, answers)

        self.assertEqual(result.correct_answers, 7)
        self.assertEqual(result.score, 70.0)
        self.assertTrue(result.passed)
        self.assertEqual(
            result.incorrect_question_ids,
            ["q7", "q8", "q9"],
        )
        self.assertEqual(
            self.remediation_service.create_remediation(
                assessment,
                result,
            ),
            [],
        )
