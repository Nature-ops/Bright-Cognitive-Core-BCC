from app.services.study_engine import StudyEngine
from tests.test_utils import build_study_session


def main():

    session = build_study_session()

    engine = StudyEngine()

    # Ensure a clean test state
    engine.progress_service.delete(session.id)
    engine.start_session(session)




    print("=" * 50)
    print("Study Exercise Test")
    print("=" * 50)

    current = engine.current_exercise()

    print("\nCurrent Exercise")
    print("----------------")

    if current is None:
        print("No exercise available.")
        return

    print(current.title)

    print("\nExercise Progress")
    print("-----------------")
    print(f"{engine.get_exercise_progress():.0f}%")

    print("\nCompleting Exercise")
    print("-------------------")
    print(current.title)

    engine.complete_exercise(
        current.id
    )

    print("\nExercise Progress")
    print("-----------------")
    print(f"{engine.get_exercise_progress():.0f}%")

    next_exercise = engine.current_exercise()

    print("\nNext Exercise")
    print("-------------")

    if next_exercise:
        print(next_exercise.title)
    else:
        print("No exercises remaining.")

    # Clean up test data
    engine.progress_service.delete(session.id)


if __name__ == "__main__":
    main()