from app.models.exercise import Exercise
from app.services.base_engine import BaseEngine
from app.services.exercise_loader import ExerciseLoader


class ExerciseEngine(BaseEngine[Exercise]):

    def __init__(self):

        super().__init__(
            ExerciseLoader()
        )

    def get_exercise(
        self,
        exercise_id: str
    ) -> Exercise:

        return self.get(exercise_id)

    def get_exercises(
        self,
    ) -> list[Exercise]:

        return self.get_all()