from app.services.study_engine import StudyEngine
from tests.test_utils import build_study_session


def main():

    session = build_study_session()

    #
    # Clean previous test state
    #

    cleanup_engine = StudyEngine()
    cleanup_engine.progress_service.delete(session.id)

    print("=" * 50)
    print("Exercise Resume Test")
    print("=" * 50)

    #
    # Engine #1
    #

    engine1 = StudyEngine()
    engine1.start_session(session)

    exercise = engine1.current_exercise()

    assert exercise is not None

    print("\nCurrent Exercise")
    print("----------------")
    print(exercise.title)

    engine1.complete_exercise(exercise.id)

    print("\nBefore Restart")
    print("--------------")
    print(
        f"Exercise Progress : "
        f"{engine1.get_exercise_progress():.0f}%"
    )

    assert exercise.id in (
        engine1.progress.completed_exercises
    )

    #
    # Simulate application restart
    #

    print("\n--- Restarting Bright ---")

    engine2 = StudyEngine()
    engine2.start_session(session)

    assert engine2.progress is not None

    print("\nAfter Restart")
    print("-------------")

    print(
        f"Exercise Progress : "
        f"{engine2.get_exercise_progress():.0f}%"
    )

    print(
        f"Completed Exercises : "
        f"{engine2.progress.completed_exercises}"
    )

    resumed_exercise = engine2.current_exercise()

    assert exercise.id in (
        engine2.progress.completed_exercises
    )

    assert resumed_exercise is None

    print("\nExercise progress restored successfully.")

    #
    # Clean test state
    #

    engine2.progress_service.delete(session.id)


if __name__ == "__main__":
    main()