from app.services.study_engine import StudyEngine
from tests.test_utils import build_study_session


def main():

    session = build_study_session()

    engine = StudyEngine()

    # Ensure clean test state
    engine.progress_service.delete(
        session.id
    )

    engine.start_session(session)

    print("=" * 50)
    print("Study Assessment Test")
    print("=" * 50)

    assert session.assessment is not None

    print("\nAssessment")
    print("----------")
    print(session.assessment.title)

    # -----------------------------------------
    # Failing attempt
    # -----------------------------------------

    failing_answers = {
        "iam-q1": "Internet Access Manager",
        "iam-q2": "IAM Group",
        "iam-q3": "Maximum access",
    }

    failed_result = engine.submit_assessment(
        failing_answers
    )

    print("\nFailing Attempt")
    print("---------------")

    print(
        f"Score     : "
        f"{failed_result.score:.0f}%"
    )

    print(
        f"Passed    : "
        f"{failed_result.passed}"
    )

    assert engine.progress is not None

    print(
        f"Completed : "
        f"{engine.progress.assessment_completed}"
    )

    assert failed_result.passed is False

    assert (
        engine.progress.assessment_completed
        is False
    )

    # -----------------------------------------
    # Passing attempt
    # -----------------------------------------

    passing_answers = {
        "iam-q1": "Identity and Access Management",
        "iam-q2": "IAM Role",
        "iam-q3": "Least privilege",
    }

    passed_result = engine.submit_assessment(
        passing_answers
    )

    print("\nPassing Attempt")
    print("---------------")

    print(
        f"Score     : "
        f"{passed_result.score:.0f}%"
    )

    print(
        f"Passed    : "
        f"{passed_result.passed}"
    )

    print(
        f"Completed : "
        f"{engine.progress.assessment_completed}"
    )

    assert passed_result.passed is True

    assert (
        engine.progress.assessment_completed
        is True
    )

    # Clean up test state
    engine.progress_service.delete(
        session.id
    )

    print()
    print("Study assessment test passed.")


if __name__ == "__main__":
    main()