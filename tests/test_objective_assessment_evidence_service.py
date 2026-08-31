from unittest import TestCase

from app.models.assessment import Assessment
from app.models.question import Question
from app.services.assessment_service import AssessmentService
from app.services.learning_gap_service import LearningGapService
from app.services.objective_assessment_evidence_service import (
    ObjectiveAssessmentEvidenceService,
)


class ObjectiveAssessmentEvidenceServiceTest(TestCase):
    def setUp(self):
        self.assessment_service = AssessmentService()
        self.learning_gap_service = LearningGapService()
        self.objective_evidence_service = (
            ObjectiveAssessmentEvidenceService()
        )

    def test_all_mapped_questions_correct_produces_one_success_per_objective(self):
        assessment = Assessment(
            id="assessment",
            title="Assessment",
            questions=[
                Question(
                    id="q1",
                    objective_id="iam-users",
                    prompt="Q1",
                    answer="Correct",
                ),
                Question(
                    id="q2",
                    objective_id="iam-users",
                    prompt="Q2",
                    answer="Correct",
                ),
                Question(
                    id="q3",
                    objective_id="iam-policies",
                    prompt="Q3",
                    answer="Correct",
                ),
                Question(id="q4", prompt="Q4", answer="Correct"),
            ],
        )
        result = self.assessment_service.evaluate(
            assessment,
            {question.id: "  correct " for question in assessment.questions},
        )

        objective_evidence = self.objective_evidence_service.create_evidence(
            assessment,
            result,
        )

        self.assertEqual(
            objective_evidence.assessed_objective_ids,
            ["iam-users", "iam-policies"],
        )
        self.assertEqual(
            objective_evidence.successful_objective_ids,
            ["iam-users", "iam-policies"],
        )

    def test_mixed_objective_is_not_successful_and_unmapped_questions_are_ignored(self):
        assessment = Assessment(
            id="assessment",
            title="Assessment",
            questions=[
                Question(
                    id="q1",
                    objective_id="iam-users",
                    prompt="Q1",
                    answer="Correct",
                ),
                Question(
                    id="q2",
                    objective_id="iam-users",
                    prompt="Q2",
                    answer="Correct",
                ),
                Question(
                    id="q3",
                    objective_id="iam-policies",
                    prompt="Q3",
                    answer="Correct",
                ),
                Question(id="q4", prompt="Q4", answer="Correct"),
            ],
        )
        result = self.assessment_service.evaluate(
            assessment,
            {
                "q1": "Correct",
                "q2": "Wrong",
                "q3": "Correct",
                "q4": "Wrong",
            },
        )

        objective_evidence = self.objective_evidence_service.create_evidence(
            assessment,
            result,
        )

        self.assertEqual(
            objective_evidence.assessed_objective_ids,
            ["iam-users", "iam-policies"],
        )
        self.assertEqual(
            objective_evidence.successful_objective_ids,
            ["iam-policies"],
        )
        self.assertEqual(
            [
                gap.objective_id
                for gap in self.learning_gap_service.create_learning_gaps(
                    assessment,
                    result,
                )
            ],
            ["iam-users"],
        )

    def test_passing_imperfect_result_has_success_and_gap_evidence(self):
        questions = [
            Question(
                id=f"q{index}",
                objective_id=("iam-users" if index < 7 else "iam-policies"),
                prompt=f"Q{index}",
                answer="Correct",
            )
            for index in range(10)
        ]
        assessment = Assessment(
            id="assessment",
            title="Assessment",
            questions=questions,
        )
        result = self.assessment_service.evaluate(
            assessment,
            {
                question.id: (
                    "Correct" if index < 7 else "Wrong"
                )
                for index, question in enumerate(questions)
            },
        )

        objective_evidence = self.objective_evidence_service.create_evidence(
            assessment,
            result,
        )

        self.assertTrue(result.passed)
        self.assertEqual(
            objective_evidence.successful_objective_ids,
            ["iam-users"],
        )
        self.assertEqual(
            [
                gap.objective_id
                for gap in self.learning_gap_service.create_learning_gaps(
                    assessment,
                    result,
                )
            ],
            ["iam-policies"],
        )
