
from app.models.learning_plan import LearningPlan
from app.services.assessment_engine import AssessmentEngine
from app.services.exercise_engine import ExerciseEngine
from app.services.planning_engine import PlanningEngine
from app.services.resource_engine import ResourceEngine
from app.services.study_session_service import StudySessionService


def iam_passing_answers() -> dict[str, str]:
    return {
        "iam-q1": "Identity and Access Management",
        "iam-q2": "IAM Role",
        "iam-q3": "Least privilege",
    }


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

    framework = planner.knowledge.framework

    milestone = planner.knowledge.get_milestone(
        "iam"
    )

    if milestone is None:
        raise RuntimeError("IAM milestone not found.")

    skills = [
        planner.knowledge.get_skill(skill_id)
        for skill_id in milestone.skill_ids
    ]

    resources = [
        planner.knowledge.get_resource(resource_id)
        for resource_id in milestone.resource_ids
    ]

    learning_plan = LearningPlan(
        framework=framework,
        milestone=milestone,
        skills=skills,
        resources=resources,
    )

    session_service = StudySessionService(
        resource_engine,
        exercise_engine,
        assessment_engine,
    )

    return session_service.create_session(
        learning_plan
    )
