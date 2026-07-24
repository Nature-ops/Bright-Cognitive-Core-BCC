from app.models.exercise import Exercise
from app.models.learning_plan import LearningPlan
from app.models.study_session import StudySession
from app.models.resource import Resource
from app.models.assessment import Assessment
from app.models.study_session import Objective
from typing import Optional


class StudySessionService:

    def __init__(
        self,
        resource_engine,
        exercise_engine,
        assessment_engine,
    ):
        
        self.resource_engine = resource_engine
        self.exercise_engine = exercise_engine
        self.assessment_engine = assessment_engine

    def _build_objectives(
        self,
        learning_plan: LearningPlan,
    ) -> list[Objective]:
        return [
            Objective(
                id=skill.id,
                title=f"Learn {skill.name}",
            )
            for skill in learning_plan.skills
        ]
    

    def _build_exercises(
        self,
        learning_plan: LearningPlan
    ) -> list[Exercise]:

        return [
            self.exercise_engine.get_exercise(exercise_id)
            for exercise_id in learning_plan.milestone.exercise_ids
        ]

    

    def _build_resources(
        self,
        learning_plan: LearningPlan,
    )-> list[Resource]:

        return learning_plan.resources

    def _build_assessment(
        self,
        learning_plan: LearningPlan,
    )-> Assessment | None:

        assessment_id = learning_plan.milestone.assessment_id

        if assessment_id is None:
            return None
        
        return self.assessment_engine.get_assessment(assessment_id)

    def create_session(
        self,
        learning_plan: LearningPlan
    ) -> StudySession:

        return StudySession(
            learning_plan=learning_plan,

            objectives=self._build_objectives(
            learning_plan
            ),

            resources=self._build_resources(
            learning_plan
            ),

            exercises=self._build_exercises(
            learning_plan
            ),

            assessment=self._build_assessment(
            learning_plan
            ),

            estimated_minutes=self._estimate_minutes(
            learning_plan
            ),
        )
     

    def _estimate_minutes(
        self,
        learning_plan: LearningPlan
    ) -> int:

        return len(learning_plan.skills) * 15

    
    