from app.services.exercise_loader import ExerciseLoader


def main():

    loader = ExerciseLoader()

    exercise = loader.load(
        "knowledge/cloud/exercises/iam.yaml"
    )

    print("=" * 50)
    print(exercise.title)
    print("=" * 50)

    print("\nDescription")
    print(exercise.description)

    print("\nSteps")

    for step in exercise.steps:
        print(f"• {step}")

    print("\nVerification")
    print(exercise.verification)


if __name__ == "__main__":
    main()