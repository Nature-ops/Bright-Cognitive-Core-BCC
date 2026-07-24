from pathlib import Path

import yaml

from app.models.exercise import Exercise


class ExerciseLoader:

    def load(
        self,
        path: str
    ) -> Exercise:

        with Path(path).open(
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(file)

        return Exercise(**data)