from pathlib import Path

from app.models.objective import Objective
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

        self._session_finished = False



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
            return None

        session = self.study_session_service.create_session(
            learning_plan
        )

        self.study_engine.start_session(
            session
        )

        return session

    
    def current_objective(self) -> Objective | None:
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



    def session_completed(self) -> bool:
        return self.study_engine.is_completed()



    def finish_session(self) -> bool:
        if self._session_finished:
            return False

        completed = self.study_engine.finish_session()

        if completed:
            self._session_finished = True

        return completed


    def advance_to_next_milestone(self):
        if not self.session_completed():
            return None

        if not self.finish_session():
            return None

        framework = self.planner.knowledge.framework

        learning_plan = (
            self.planner.create_learning_plan_for_framework(
                framework.id
            )
        )

        if learning_plan is None:
            return None

        session = (
            self.study_session_service.create_session(
                learning_plan
            )
        )

        self.study_engine.start_session(session)

        self._session_finished = False

        return session



    


    def objectives(self) -> list[Objective]:

        assert self.study_engine.session is not None

        return self.study_engine.session.objectives


    def completed_objectives(self) -> list[str]:

        assert self.study_engine.progress is not None

        return self.study_engine.progress.completed_objectives


    def resources(self):

        assert self.study_engine.session is not None

        return self.study_engine.session.learning_plan.resources


    def exercises(self):

        assert self.study_engine.session is not None

        return self.study_engine.session.exercises


    def current_assessment(self):
        return self.study_engine.current_assessment()

    

    def current_exercise(self):
        return self.study_engine.current_exercise()


    def learning_state(self):
        objective = self.current_objective()

        if objective is not None:
            return "objective", objective

        exercise = self.current_exercise()

        if exercise is not None:
            return "exercise", exercise


        assessment = self.current_assessment()

        if assessment is not None:
            return "assessment", assessment

        return "completed", None


    def complete_current_exercise(self):

        exercise = (
            self.study_engine.current_exercise()
        )

        if exercise is None:
            return None

        self.study_engine.complete_exercise(
            exercise.id
        )

        return exercise


    def exercise_progress(self) -> float:

        return (
            self.study_engine.get_exercise_progress()
        )



    def milestone_progress(self) -> float:

        assert self.study_engine.session is not None

        framework = (
            self.study_engine.session.learning_plan.framework
        )

        milestone_ids = [
            milestone.id
            for milestone in framework.milestones
        ]

        return self.study_engine.framework_progress_service.milestone_progress(
            framework.id,
            milestone_ids,
        )


    def submit_assessment(
        self,
        answers,
    ):

        print()

        
        return self.study_engine.submit_assessment(
            answers
        )
