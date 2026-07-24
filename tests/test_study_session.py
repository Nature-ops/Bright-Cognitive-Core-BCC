from app.services.planning_engine import PlanningEngine
from app.services.study_session_service import StudySessionService
from app.services.resource_engine import ResourceEngine
from app.services.exercise_engine import ExerciseEngine
from app.services.assessment_engine import AssessmentEngine
from app.services.file_loader import FileLoader


def print_study_session(session):

    print("=" * 50)
    print("Today's Study Session")
    print("=" * 50)

    print("\nMilestone")
    print("---------")
    print(session.learning_plan.milestone.title)

    print("\nDescription")
    print("-----------")
    print(session.learning_plan.milestone.description)

    print("\nObjectives")
    print("----------")
    for objective in session.objectives:
        print(f"✓ {objective.title}")

    print("\nResources")
    print("---------")
    for resource in session.learning_plan.resources:
        print(f"• {resource.title}")
        print(f"  {resource.url}")

    print("\nExercises")
    print("---------")

    print("\nAssessment")
    print("----------")

    if session.assessment:
        print(session.assessment.title)

    else:
        print("No assessment available")

    for exercise in session.exercises:

        print(f"\n{exercise.title}")
        print("-" * len(exercise.title))

        print(exercise.description)

        print("\nSteps")

        for step in exercise.steps:
            print(f"☐ {step}")

        print("\nVerification")
        print(exercise.verification)

    print("\nEstimated Time")
    print("--------------")
    print(f"{session.estimated_minutes} minutes")


def main():

    planner = PlanningEngine()

    planner.load_framework(
    "knowledge/cloud/frameworks/aws-sa.yaml"
    )

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

    learning_plan = planner.create_learning_plan_for_framework(
        "aws-sa"
    )

    if learning_plan is None:
        print("Framework completed.")
        return


    service = StudySessionService(
        resource_engine,
        exercise_engine,
        assessment_engine,
    )

    session = service.create_session(
        learning_plan
    )

    print_study_session(session)


if __name__ == "__main__":
    main()