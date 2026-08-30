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
    print("Resume Session Test")
    print("=" * 50)

    # -----------------------------------------
    # First Bright instance
    # -----------------------------------------

    engine1 = StudyEngine()

    engine1.start_session(session)

    first = engine1.current_objective()

    assert first is not None

    print("\nFirst Objective")
    print("----------------")
    print(first.title)

    engine1.complete_objective(
        first.id
    )

    print("\nCompleted:")
    print(first.title)

    # Do NOT finish the session.
    # We want the progress to remain persisted.

    # -----------------------------------------
    # Simulate restarting Bright
    # -----------------------------------------

    print("\n--- Restarting Bright ---")

    engine2 = StudyEngine()

    # Important:
    # load the session before asking for an objective.
    engine2.start_session(session)

    resumed = engine2.current_objective()

    assert resumed is not None

    print("\nResumed Objective")
    print("-----------------")
    print(resumed.title)

    # Complete the remaining objective.
    engine2.complete_objective(
        resumed.id
    )

    # -----------------------------------------
    # Complete exercises
    # -----------------------------------------

    print("\nExercises")
    print("---------")

    exercise = engine2.current_exercise()

    while exercise:

        print(
            f"Completing: {exercise.title}"
        )

        engine2.complete_exercise(
            exercise.id
        )

        print(
            f"Exercise Progress: "
            f"{engine2.get_exercise_progress():.0f}%"
        )

        exercise = engine2.current_exercise()

    print("\nAssessment")
    print("----------")

    if session.assessment is not None:

        answers = iam_passing_answers()

        result = engine2.submit_assessment(
            answers
        )

        print(session.assessment.title)

        print(
            f"Score  : {result.score:.0f}%"
        )

        print(
            f"Passed : {result.passed}"
        )

    else:

        print("No assessment required.")





    # -----------------------------------------
    # Verify final state
    # -----------------------------------------

    print("\nSession Status")
    print("--------------")

    print(
        f"Completed : "
        f"{engine2.is_completed()}"
    )

    print(
        f"Finished  : "
        f"{engine2.finish_session()}"
    )


if __name__ == "__main__":
    main()
