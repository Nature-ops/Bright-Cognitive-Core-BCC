from app.services.study_engine import StudyEngine

from tests.test_utils import build_study_session


def main():

    session = build_study_session()

    engine = StudyEngine()

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

    print("\nSession Status")
    print("--------------")

    print(f"Completed : {engine.is_completed()}")

    print(f"Finished  : {engine.finish_session()}")


if __name__ == "__main__":
    main()