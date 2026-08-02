from app.core.learning.session_controller import SessionController


def main():

    print("=" * 50)
    print("Session Controller Test")
    print("=" * 50)

    controller = SessionController(
        "knowledge/cloud/frameworks/aws-sa.yaml"
    )

    session = controller.start()

    print("\nFramework")
    print("---------")

    print(
        session.learning_plan.framework.name
    )

    print("\nCurrent Milestone")
    print("-----------------")

    print(
        session.learning_plan.milestone.title
    )

    print("\nObjectives")
    print("----------")

    for objective in session.objectives:

        print(f"• {objective.title}")

    print("\nExercises")
    print("---------")

    for exercise in session.exercises:

        print(f"• {exercise.title}")

    print("\nAssessment")
    print("----------")

    if session.assessment is None:

        print("No assessment.")

    else:

        print(
            session.assessment.title
        )

    print("\nController started successfully.")


if __name__ == "__main__":
    main()