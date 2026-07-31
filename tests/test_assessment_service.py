from app.models.assessment import Assessment
from app.models.question import Question
from app.services.assessment_service import AssessmentService


def build_assessment() -> Assessment:

    return Assessment(
        id="iam-test",
        title="IAM Assessment",
        description="Test your IAM knowledge.",
        passing_score=70,
        questions=[
            Question(
                id="q1",
                prompt="What does IAM stand for?",
                options=[
                    "Identity and Access Management",
                    "Internet Access Manager",
                    "Instance Access Management",
                ],
                answer="Identity and Access Management",
                explanation=(
                    "IAM stands for Identity and Access Management."
                ),
            ),
            Question(
                id="q2",
                prompt="Which IAM identity can be assumed?",
                options=[
                    "Role",
                    "Group",
                    "Policy",
                ],
                answer="Role",
                explanation=(
                    "IAM roles can be assumed by trusted identities."
                ),
            ),
            Question(
                id="q3",
                prompt="Which principle should IAM permissions follow?",
                options=[
                    "Least privilege",
                    "Maximum access",
                    "Public access",
                ],
                answer="Least privilege",
                explanation=(
                    "Permissions should follow the principle "
                    "of least privilege."
                ),
            ),
        ],
    )


def test_passing_assessment():

    assessment = build_assessment()

    service = AssessmentService()

    answers = {
        "q1": "Identity and Access Management",
        "q2": "Role",
        "q3": "Least privilege",
    }

    result = service.evaluate(
        assessment,
        answers,
    )

    print("=" * 50)
    print("Passing Assessment Test")
    print("=" * 50)

    print(f"Correct : {result.correct_answers}")
    print(f"Total   : {result.total_questions}")
    print(f"Score   : {result.score:.0f}%")
    print(f"Passed  : {result.passed}")

    assert result.correct_answers == 3
    assert result.total_questions == 3
    assert result.score == 100.0
    assert result.passed is True


def test_failing_assessment():

    assessment = build_assessment()

    service = AssessmentService()

    answers = {
        "q1": "Identity and Access Management",
        "q2": "Group",
        "q3": "Maximum access",
    }

    result = service.evaluate(
        assessment,
        answers,
    )

    print()
    print("=" * 50)
    print("Failing Assessment Test")
    print("=" * 50)

    print(f"Correct : {result.correct_answers}")
    print(f"Total   : {result.total_questions}")
    print(f"Score   : {result.score:.0f}%")
    print(f"Passed  : {result.passed}")

    assert result.correct_answers == 1
    assert result.total_questions == 3

    assert round(result.score, 2) == 33.33

    assert result.passed is False


def main():

    test_passing_assessment()

    test_failing_assessment()

    test_exact_passing_score()

    print()
    print("AssessmentService tests passed.")




def test_exact_passing_score():

        questions = []

        answers = {}

        for index in range(10):

            question_id = f"q{index + 1}"

            questions.append(
                Question(
                    id=question_id,
                    prompt=f"Question {index + 1}",
                    options=[
                        "Correct",
                        "Wrong",
                    ],
                    answer="Correct",
                )
            )

            if index < 7:
                answers[question_id] = "Correct"
            else:
                answers[question_id] = "Wrong"

        assessment = Assessment(
            id="boundary-test",
            title="Passing Score Boundary Test",
            passing_score=70,
            questions=questions,
        )

        service = AssessmentService()

        result = service.evaluate(
            assessment,
            answers,
        )

        print()
        print("=" * 50)
        print("Passing Score Boundary Test")
        print("=" * 50)

        print(f"Correct : {result.correct_answers}")
        print(f"Total   : {result.total_questions}")
        print(f"Score   : {result.score:.0f}%")
        print(f"Passed  : {result.passed}")

        assert result.correct_answers == 7
        assert result.total_questions == 10
        assert result.score == 70.0
        assert result.passed is True


if __name__ == "__main__":
    main()