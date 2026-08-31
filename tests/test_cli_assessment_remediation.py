from contextlib import redirect_stdout
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from app.cli.cli import BrightCLI
from app.models.assessment import Assessment
from app.models.assessment_remediation import AssessmentRemediation
from app.models.assessment_result import AssessmentResult
from app.models.question import Question


class AssessmentControllerStub:
    def __init__(self, result: AssessmentResult):
        self.result = result
        self.answers = None

    def submit_assessment(self, answers):
        self.answers = answers

        return self.result


class CLIAssessmentRemediationTest(TestCase):
    def test_failed_assessment_renders_structured_remediation(self):
        assessment = Assessment(
            id="assessment",
            title="Assessment",
            questions=[
                Question(
                    id="q1",
                    prompt="Which identity is assumable?",
                    options=["IAM Group", "IAM Role"],
                    answer="IAM Role",
                    explanation="IAM roles can be assumed.",
                )
            ],
        )
        result = AssessmentResult(
            assessment_id="assessment",
            correct_answers=0,
            total_questions=1,
            score=0.0,
            passed=False,
            incorrect_question_ids=["q1"],
            remediation=[
                AssessmentRemediation(
                    question_id="q1",
                    prompt="Which identity is assumable?",
                    explanation="IAM roles can be assumed.",
                )
            ],
        )
        controller = AssessmentControllerStub(result)
        cli = BrightCLI(controller)
        output = StringIO()

        with patch("builtins.input", side_effect=["1"]):
            with redirect_stdout(output):
                cli.run_assessment(assessment)

        rendered_output = output.getvalue()

        self.assertEqual(controller.answers, {"q1": "IAM Group"})
        self.assertIn("Review before retrying:", rendered_output)
        self.assertIn("- Which identity is assumable?", rendered_output)
        self.assertIn("IAM roles can be assumed.", rendered_output)
