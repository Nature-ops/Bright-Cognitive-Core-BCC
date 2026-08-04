from app.models.assessment import Assessment
from app.models.assessment_result import AssessmentResult


class AssessmentService:

    def evaluate(
        self,
        assessment: Assessment,
        answers: dict[str, str],
    ) -> AssessmentResult:

        correct_answers = 0

        for question in assessment.questions:

            submitted_answer = answers.get(
                question.id
            )

            if (
                submitted_answer is not None
                and submitted_answer.strip().casefold()
                == question.answer.strip().casefold()
            ):
                correct_answers += 1

    

        total_questions = len(
            assessment.questions
        )

        if total_questions == 0:
            score = 0.0

        else:
            score = (
                correct_answers
                / total_questions
                * 100
            )

        passed = (
            score >= assessment.passing_score
        )



        for question in assessment.questions:

            submitted_answer = answers.get(question.id)

            print()
            

            if submitted_answer == question.answer:
                correct_answers += 1




        return AssessmentResult(
            assessment_id=assessment.id,
            answers=answers,
            correct_answers=correct_answers,
            total_questions=total_questions,
            score=score,
            passed=passed,
        )