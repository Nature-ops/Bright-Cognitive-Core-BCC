from app.services.planning_engine import PlanningEngine
from app.services.progress_service import ProgressService
from app.services.study_engine import StudyEngine
from app.services.study_session_service import StudySessionService
from app.services.resource_engine import ResourceEngine
from app.services.exercise_engine import ExerciseEngine
from app.services.assessment_engine import AssessmentEngine


def main():

    framework_path = (
        "knowledge/cloud/frameworks/aws-sa.yaml"
    )

    framework_id = "aws-sa"

    progress_service = ProgressService()

    # Preserve the user's real framework progress.
    original_records = progress_service.load()

    session = None

    try:

        # -----------------------------------------
        # Establish controlled starting state
        # -----------------------------------------

        progress = progress_service.get_progress(
            framework_id
        )

        progress.completed_milestones = [
            "aws-fundamentals"
        ]

        progress_service.update_progress(
            progress
        )

        # -----------------------------------------
        # Build planner
        # -----------------------------------------

        planner = PlanningEngine()

        planner.load_framework(
            framework_path
        )

        learning_plan = (
            planner.create_learning_plan_for_framework(
                framework_id
            )
        )

        assert learning_plan is not None
        assert learning_plan.milestone.id == "iam"

        print("=" * 50)
        print("End-to-End Study Progression Test")
        print("=" * 50)

        print("\nSelected Milestone")
        print("------------------")

        print(
            f"{learning_plan.milestone.title}"
        )

        # -----------------------------------------
        # Build StudySession dependencies
        # -----------------------------------------

        resource_engine = ResourceEngine()

        resource_engine.load_directory(
            "knowledge/cloud/resources"
        )

        exercise_engine = ExerciseEngine()

        exercise_engine.load_directory(
            "knowledge/cloud/exercises"
        )

        assessment_engine = AssessmentEngine()

        assessment_engine.load_directory(
            "knowledge/cloud/assessments"
        )

        session_service = StudySessionService(
            resource_engine,
            exercise_engine,
            assessment_engine,
        )

        session = session_service.create_session(
            learning_plan
        )

        # -----------------------------------------
        # Start StudyEngine
        # -----------------------------------------

        engine = StudyEngine()

        # Ensure no previous temporary session state
        # affects this test.
        engine.progress_service.delete(
            session.id
        )

        engine.start_session(
            session
        )

        # -----------------------------------------
        # Complete objectives
        # -----------------------------------------

        while True:

            objective = engine.current_objective()

            if objective is None:
                break

            print(
                f"Completing objective: "
                f"{objective.title}"
            )

            engine.complete_objective(
                objective.id
            )

        # -----------------------------------------
        # Complete exercises
        # -----------------------------------------

        while True:

            exercise = engine.current_exercise()

            if exercise is None:
                break

            print(
                f"Completing exercise: "
                f"{exercise.title}"
            )

            engine.complete_exercise(
                exercise.id
            )

        # -----------------------------------------
        # Complete assessment
        # -----------------------------------------

        assert session.assessment is not None

        answers = {
            "iam-q1": "Identity and Access Management",
            "iam-q2": "IAM Role",
            "iam-q3": "Least privilege",
        }

        result = engine.submit_assessment(
            answers
        )

        print(
            f"Assessment score: "
            f"{result.score:.0f}%"
        )

        assert result.passed is True

        # -----------------------------------------
        # Finish IAM session
        # -----------------------------------------

        assert engine.is_completed() is True

        finished = engine.finish_session()

        assert finished is True

        print("\nIAM Session")
        print("-----------")
        print("Completed successfully.")

        # -----------------------------------------
        # Verify framework progress
        # -----------------------------------------

        progress = progress_service.get_progress(
            framework_id
        )

        print("\nFramework Progress")
        print("------------------")

        print(
            f"Completed Milestones : "
            f"{progress.completed_milestones}"
        )

        assert (
            "iam"
            in progress.completed_milestones
        )

        # -----------------------------------------
        # Ask Bright what comes next
        # -----------------------------------------

        next_plan = (
            planner.create_learning_plan_for_framework(
                framework_id
            )
        )

        assert next_plan is not None

        print("\nNext Milestone")
        print("--------------")

        print(
            next_plan.milestone.title
        )

        assert (
            next_plan.milestone.id
            == "ec2"
        )

        print(
            "\nEnd-to-end study progression "
            "works successfully."
        )

    finally:

        # -----------------------------------------
        # Restore real framework progress
        # -----------------------------------------

        progress_service.save(
            original_records
        )

        # Remove temporary StudyProgress if the
        # session was successfully constructed.
        if session is not None:

            cleanup_engine = StudyEngine()

            cleanup_engine.progress_service.delete(
                session.id
            )


if __name__ == "__main__":
    main()