from app.services.study_engine import StudyEngine
from app.services.progress_service import ProgressService
from tests.test_utils import build_study_session


def main():

    session = build_study_session()

    framework_id = session.learning_plan.framework.id
    milestone_id = session.learning_plan.milestone.id

    framework_progress = ProgressService()

    # Preserve the real framework progress before the test.
    original_records = framework_progress.load()

    try:

        # Remove IAM from completed milestones for a predictable test.
        progress = framework_progress.get_progress(
            framework_id
        )

        if milestone_id in progress.completed_milestones:
            progress.completed_milestones.remove(
                milestone_id
            )

            framework_progress.update_progress(
                progress
            )

        # Clean temporary study-session progress.
        engine = StudyEngine()

        engine.progress_service.delete(
            session.id
        )

        engine.start_session(session)

        print("=" * 50)
        print("Milestone Completion Test")
        print("=" * 50)

        print("\nBefore Session")
        print("--------------")

        progress = framework_progress.get_progress(
            framework_id
        )

        print(
            f"Completed Milestones : "
            f"{progress.completed_milestones}"
        )

        assert (
            milestone_id
            not in progress.completed_milestones
        )

        # Complete objectives.
        while True:

            objective = engine.current_objective()

            if objective is None:
                break

            engine.complete_objective(
                objective.id
            )

        # Complete exercises.
        while True:

            exercise = engine.current_exercise()

            if exercise is None:
                break

            engine.complete_exercise(
                exercise.id
            )

        # Pass required assessment.
        if session.assessment is not None:

            answers = {
                "iam-q1": "Identity and Access Management",
                "iam-q2": "IAM Role",
                "iam-q3": "Least privilege",
            }

            result = engine.submit_assessment(
                answers
            )

            assert result.passed is True

        print("\nBefore Finish")
        print("-------------")
        print(
            f"Session Completed : "
            f"{engine.is_completed()}"
        )

        assert engine.is_completed() is True

        finished = engine.finish_session()

        assert finished is True

        # Reload framework progress from disk.
        progress = framework_progress.get_progress(
            framework_id
        )

        print("\nAfter Finish")
        print("------------")

        print(
            f"Completed Milestones : "
            f"{progress.completed_milestones}"
        )

        assert (
            milestone_id
            in progress.completed_milestones
        )

        print(
            "\nMilestone completion recorded successfully."
        )

    finally:

        # Restore the exact framework progress that existed
        # before this test ran.
        framework_progress.save(
            original_records
        )

        # Also remove temporary study-session state.
        cleanup_engine = StudyEngine()

        cleanup_engine.progress_service.delete(
            session.id
        )


if __name__ == "__main__":
    main()