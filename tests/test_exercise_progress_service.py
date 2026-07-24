from app.services.exercise_progress_service import ExerciseProgressService


def print_result(title, result):

    print("=" * 50)
    print(title)
    print("=" * 50)

    print(f"Exercise : {result.exercise_id}")
    print(f"Completed: {result.completed}")
    print(f"Completed At: {result.completed_at}")
    print(f"Notes: {result.notes}")
    print()


def main():

    service = ExerciseProgressService()

    # Initial state
    result = service.get_result("iam-lab")
    print_result("Initial Status", result)

    # Complete the exercise
    service.complete_exercise("iam-lab")

    # Verify completion
    result = service.get_result("iam-lab")
    print_result("After Completion", result)

    # Simulate restarting the application
    service = ExerciseProgressService()

    result = service.get_result("iam-lab")
    print_result("Reloaded From Disk", result)


if __name__ == "__main__":
    main()