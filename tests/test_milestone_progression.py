from app.services.planning_engine import PlanningEngine
from app.services.progress_service import ProgressService


def main():

    framework_path = (
        "knowledge/cloud/frameworks/aws-sa.yaml"
    )

    framework_id = "aws-sa"

    progress_service = ProgressService()

    # Preserve real framework progress.
    original_records = progress_service.load()

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

        planner = PlanningEngine()

        planner.load_framework(
            framework_path
        )

        print("=" * 50)
        print("Milestone Progression Test")
        print("=" * 50)

        # -----------------------------------------
        # Before IAM completion
        # -----------------------------------------

        plan = (
            planner.create_learning_plan_for_framework(
                framework_id
            )
        )

        assert plan is not None

        print("\nBefore IAM Completion")
        print("---------------------")

        print(
            f"Next Milestone : "
            f"{plan.milestone.title}"
        )

        print(
            f"Milestone ID   : "
            f"{plan.milestone.id}"
        )

        assert plan.milestone.id == "iam"

        # -----------------------------------------
        # Complete IAM
        # -----------------------------------------

        progress_service.complete_milestone(
            framework_id=framework_id,
            milestone_id="iam",
        )

        # -----------------------------------------
        # Ask planner again
        # -----------------------------------------

        next_plan = (
            planner.create_learning_plan_for_framework(
                framework_id
            )
        )

        assert next_plan is not None

        print("\nAfter IAM Completion")
        print("--------------------")

        print(
            f"Next Milestone : "
            f"{next_plan.milestone.title}"
        )

        print(
            f"Milestone ID   : "
            f"{next_plan.milestone.id}"
        )

        assert next_plan.milestone.id == "ec2"

        print(
            "\nAutomatic milestone progression "
            "works successfully."
        )

    finally:

        # Restore the exact framework progress
        # that existed before this test.
        progress_service.save(
            original_records
        )


if __name__ == "__main__":
    main()