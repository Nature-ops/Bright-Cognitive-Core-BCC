import json
from datetime import UTC, datetime
from pathlib import Path

from app.models.exercise_result import ExerciseResult

class ExerciseProgressService:

    def __init__(self):

        self.progress_file = Path(
            "data/exercise_progress.json"
        )

        if not self.progress_file.exists():
            self.progress_file.write_text("[]")



    def load(self) -> list[ExerciseResult]:

        try:

            with self.progress_file.open(
            "r",
            encoding="utf-8"
            ) as file:

                data = json.load(file)

            return [
                ExerciseResult(**item)
                for item in data
            ]

        except (
            json.JSONDecodeError,
            FileNotFoundError
        ):
            return []

    def save(
        self,
        results: list[ExerciseResult]
    ) -> None:

        with self.progress_file.open(
            "w",
            encoding="utf-8"
            ) as file:

            json.dump(
                [
                    result.model_dump(mode="json")
                    for result in results
                ],
                file,
                indent=2
            )



    def get_result(
        self,
        exercise_id: str
    ) -> ExerciseResult:

        results = self.load()

        for result in results:

            if result.exercise_id == exercise_id:
                return result

        result = ExerciseResult(
            exercise_id=exercise_id
        )

        results.append(result)

        self.save(results)

        return result


    def update_result(
        self,
        result: ExerciseResult
    ) -> None:

        results = self.load()

        updated = False

        for index, current in enumerate(results):

            if current.exercise_id == result.exercise_id:

                results[index] = result
                updated = True
                break

        if not updated:
                results.append(result)

        self.save(results)



    def complete_exercise(
        self,
        exercise_id: str
    ) -> None:

        result = self.get_result(exercise_id)

        if result.completed:
            return

        result.completed = True

        result.completed_at = datetime.now(
            UTC
        )

        self.update_result(result)