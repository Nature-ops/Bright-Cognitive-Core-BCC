from app.services.study_engine import StudyEngine
from tests.test_utils import (
    build_study_session,
    iam_passing_answers,
)


def main():

    session = build_study_session()

    # -----------------------------------------
    # Clean previous test state
    # -----------------------------------------

    cleanup_engine = StudyEngine()

    cleanup_engine.progress_service.delete(
        session.id
    )

    print("=" * 50)
    print("Assessment Resume Test")
    print("=" * 50)

    # -----------------------------------------
    # First Bright instance
    # -----------------------------------------

    engine1 = StudyEngine()
    engine1.start_session(session)

    assert session.assessment is not None

    passing_answers = iam_passing_answers()

    result = engine1.submit_assessment(
        passing_answers
    )

    print("\nBefore Restart")
    print("--------------")

    print(
        f"Assessment Score     : "
        f"{result.score:.0f}%"
    )

    print(
        f"Assessment Passed    : "
        f"{result.passed}"
    )

    assert engine1.progress is not None

    print(
        f"Assessment Completed : "
        f"{engine1.progress.assessment_completed}"
    )

    assert result.passed is True
    assert (
        engine1.progress.assessment_completed
        is True
    )

    # IMPORTANT:
    # Do not call finish_session().
    # We need the persisted progress for the restart test.

    # -----------------------------------------
    # Simulate restarting Bright
    # -----------------------------------------

    print("\n--- Restarting Bright ---")

    engine2 = StudyEngine()
    engine2.start_session(session)

    assert engine2.progress is not None

    print("\nAfter Restart")
    print("-------------")

    print(
        f"Assessment Completed : "
        f"{engine2.progress.assessment_completed}"
    )

    assert (
        engine2.progress.assessment_completed
        is True
    )

    print(
        "\nAssessment progress restored successfully."
    )

    # -----------------------------------------
    # Clean test state
    # -----------------------------------------

    engine2.progress_service.delete(
        session.id
    )


if __name__ == "__main__":
    main()
