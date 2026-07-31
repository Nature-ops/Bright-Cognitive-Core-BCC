from app.services.study_engine import StudyEngine
from tests.test_utils import build_study_session


def main():

    session = build_study_session()

    engine = StudyEngine()

    # Ensure clean test state
    engine.progress_service.delete(session.id)

    engine.start_session(session)

    print("=" * 50)
    print("Session Completion Test")
    print("=" * 50)

    # Complete all objectives
    objective = engine.current_objective()

    while objective:

        engine.complete_objective(
            objective.id
        )

        objective = engine.current_objective()

    print("\nAfter Objectives")
    print("----------------")

    print(
        f"Objective Progress : "
        f"{engine.get_progress():.0f}%"
    )

    print(
        f"Exercise Progress  : "
        f"{engine.get_exercise_progress():.0f}%"
    )

    print(
        f"Session Completed  : "
        f"{engine.is_completed()}"
    )

    # Session must NOT be complete yet
    assert engine.is_completed() is False

    # Complete all exercises
    exercise = engine.current_exercise()

    while exercise:

        engine.complete_exercise(
            exercise.id
        )

        exercise = engine.current_exercise()

    print("\nAfter Exercises")
    print("---------------")

    print(
        f"Objective Progress : "
        f"{engine.get_progress():.0f}%"
    )

    print(
        f"Exercise Progress  : "
        f"{engine.get_exercise_progress():.0f}%"
    )

    print(
        f"Session Completed  : "
        f"{engine.is_completed()}"
    )

    # Now it MUST be complete
    assert engine.is_completed() is False


    print("\nAfter Failed Assessment")
    print("-----------------------")

    failing_answers = {
        "iam-q1": "Internet Access Manager",
        "iam-q2": "IAM Group",
        "iam-q3": "Maximum access",
    }

    failed_result = engine.submit_assessment(
        failing_answers
    )

    print(
        f"Assessment Score   : "
        f"{failed_result.score:.0f}%"
    )

    print(
        f"Assessment Passed  : "
        f"{failed_result.passed}"
    )

    print(
        f"Session Completed  : "
        f"{engine.is_completed()}"
    )

    assert failed_result.passed is False
    assert engine.is_completed() is False

    print("\nAfter Passed Assessment")
    print("-----------------------")

    passing_answers = {
        "iam-q1": "Identity and Access Management",
        "iam-q2": "IAM Role",
        "iam-q3": "Least privilege",
    }

    passed_result = engine.submit_assessment(
        passing_answers
    )

    print(
        f"Assessment Score   : "
        f"{passed_result.score:.0f}%"
    )

    print(
        f"Assessment Passed  : "
        f"{passed_result.passed}"
    )

    print(
        f"Session Completed  : "
        f"{engine.is_completed()}"
    )

    assert passed_result.passed is True
    assert engine.is_completed() is True

    finished = engine.finish_session()

    assert finished is True

    print("\nSession finished successfully.")

if __name__ == "__main__":
    main()