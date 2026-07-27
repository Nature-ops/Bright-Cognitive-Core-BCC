from app.services.assessment_engine import AssessmentEngine
from app.services.exercise_engine import ExerciseEngine
from app.services.planning_engine import PlanningEngine
from app.services.resource_engine import ResourceEngine
from app.services.study_session_service import StudySessionService


def build_study_session():

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
        raise RuntimeError("Framework completed.")

    session_service = StudySessionService(
        resource_engine,
        exercise_engine,
        assessment_engine,
    )

    return session_service.create_session(
        learning_plan
    )