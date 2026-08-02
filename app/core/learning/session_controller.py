from pathlib import Path
from app.cli.renderer import BrightRenderer

from app.services.assessment_engine import AssessmentEngine
from app.services.exercise_engine import ExerciseEngine
from app.services.planning_engine import PlanningEngine
from app.services.resource_engine import ResourceEngine
from app.services.study_engine import StudyEngine
from app.services.study_session_service import StudySessionService



class SessionController:

    def __init__(
        self,
        framework_path: str | Path,
    ):

        self.framework_path = Path(
            framework_path
        )

        self.planner = PlanningEngine()

        self.resource_engine = ResourceEngine()

        self.exercise_engine = ExerciseEngine()

        self.assessment_engine = AssessmentEngine()

        self.study_session_service = (
            StudySessionService(
                self.resource_engine,
                self.exercise_engine,
                self.assessment_engine,
            )
        )

        self.study_engine = StudyEngine()



    def start(self):

        # Load framework
        self.planner.load_framework(
            self.framework_path
        )

        knowledge_root = (
            self.framework_path.parent.parent
        )

        # Load supporting knowledge
        self.resource_engine.load_directory(
            knowledge_root / "resources"
        )

        self.exercise_engine.load_directory(
            knowledge_root / "exercises"
        )

        self.assessment_engine.load_directory(
            knowledge_root / "assessments"
        )

        framework = self.planner.knowledge.framework

        learning_plan = (
            self.planner.create_learning_plan_for_framework(
                framework.id
            )
        )

        if learning_plan is None:
            raise RuntimeError(
                "No learning plan available."
            )

        session = self.study_session_service.create_session(
            learning_plan
        )

        self.study_engine.start_session(
            session
        )

        return session

    
    def current_objective(self):
        return self.study_engine.current_objective()


    def complete_current_objective(self):

        objective = self.study_engine.current_objective()

        if objective is None:
            return None

        self.study_engine.complete_objective(
            objective.id
        )

        return objective


    def objective_progress(self) -> float:
        return self.study_engine.get_progress()



    # def next_activity(self) -> Activity:

        objective = self.study_engine.current_objective()

        if objective is not None:
            return Activity(
                type=ActivityType.OBJECTIVE,
                item=objective,
            )

        exercise = self.study_engine.current_exercise()

        if exercise is not None:
            return Activity(
                type=ActivityType.EXERCISE,
                item=exercise,
            )

        assessment = self.study_engine.current_assessment()

        if assessment is not None:
            return Activity(
                type=ActivityType.ASSESSMENT,
                item=assessment,
            )

        return Activity(
            type=ActivityType.COMPLETED
        )