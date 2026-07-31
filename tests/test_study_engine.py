from app.services.study_engine import StudyEngine

from tests.test_utils import build_study_session


def main():

    session = build_study_session()

    engine = StudyEngine()

    engine.progress_service.delete(session.id)

    engine.start_session(session)

    print("=" * 50)
    print("Study Engine")
    print("=" * 50)

    print()

    current = engine.current_objective()

    if current:
        print(f"Current Objective : {current.title}")
    else:
        print("Current Objective : None")

    print(f"Progress          : {engine.get_progress():.0f}%")

    print()

    while current:

        print(f"Completing: {current.title}")

        engine.complete_objective(current.id)

        print(
            f"Progress: {engine.get_progress():.0f}%"
        )

        current = engine.current_objective()


    print()

    print("Exercise Status")
    print("---------------")

    exercise = engine.current_exercise()

    while exercise:

        print(f"Completing: {exercise.title}")

        engine.complete_exercise(exercise.id)

        print(
            f"Exercise Progress: "
            f"{engine.get_exercise_progress():.0f}%"
        )

        exercise = engine.current_exercise()

        print()

        print("Assessment Status")
        print("-----------------")

        if session.assessment is not None:

            answers = {
                    "iam-q1": "Identity and Access Management",
                    "iam-q2": "IAM Role",
                    "iam-q3": "Least privilege",
            }

            result = engine.submit_assessment(
                    answers
            )

            print(
                    f"Assessment : {session.assessment.title}"
            )

            print(
                    f"Score      : {result.score:.0f}%"
            )
            print(
                    f"Passed     : {result.passed}"
            )

        else:

            print("No assessment required.")

    

    print()

    print("\nSession Status")
    print("--------------")

    print(f"Completed : {engine.is_completed()}")

    print(f"Finished  : {engine.finish_session()}")


if __name__ == "__main__":
    main()