from app.models.study_progress import StudyProgress
from app.services.study_progress_service import StudyProgressService


def main():

    service = StudyProgressService()

    progress = StudyProgress(
        session_id="test-session"
    )

    print("=" * 50)
    print("Study Progress Service Test")
    print("=" * 50)

    print("\nSaving progress...")
    service.save(progress)

    print("Saved.")

    print("\nChecking if progress exists...")
    print(service.exists("test-session"))

    print("\nLoading progress...")
    loaded = service.load("test-session")

    if loaded:
        print("Loaded successfully.")
        print(f"Session ID: {loaded.session_id}")
        print(f"Objectives: {loaded.completed_objectives}")
        print(f"Exercises: {loaded.completed_exercises}")
        print(f"Assessment: {loaded.assessment_completed}")
    else:
        print("Failed to load progress.")

    print("\nDeleting progress...")
    service.delete("test-session")

    print("Deleted.")

    print("\nExists after delete?")
    print(service.exists("test-session"))


if __name__ == "__main__":
    main()