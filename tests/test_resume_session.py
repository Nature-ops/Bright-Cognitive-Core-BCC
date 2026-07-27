from app.services.study_engine import StudyEngine
from tests.test_utils import build_study_session


def main():

    session = build_study_session()

    print("=" * 50)
    print("Resume Session Test")
    print("=" * 50)

    #
    # First application instance
    #

    engine1 = StudyEngine()

    engine1.start_session(session)

    first = engine1.current_objective()

    assert first is not None

    print("\nFirst Objective")
    print("----------------")
    print(first.title)

    engine1.complete_objective(first.id)

    print("\nCompleted:")
    print(first.title)

    #
    # Simulate closing Bright
    #

    print("\n--- Restarting Bright ---")

    #
    # Second application instance
    #

    engine2 = StudyEngine()

    engine2.start_session(session)

    resumed = engine2.current_objective()

    assert resumed is not None

    print("\nResumed Objective")
    print("-----------------")
    print(resumed.title)

    #
    # Finish the session
    #

    engine2.complete_objective(resumed.id)

    print("\nSession Status")
    print("--------------")
    print(f"Completed : {engine2.is_completed()}")
    print(f"Finished  : {engine2.finish_session()}")


if __name__ == "__main__":
    main()