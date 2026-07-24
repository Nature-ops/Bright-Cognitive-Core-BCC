from app.services.exercise_engine import ExerciseEngine


def main():

    engine = ExerciseEngine()

    engine.load_directory(
        "knowledge/cloud/exercises"
    )

    print("=" * 50)
    print("Available Exercises")
    print("=" * 50)

    for exercise in engine.get_exercises():

        print(f"\n{exercise.id}")
        print(exercise.title)


if __name__ == "__main__":
    main()