from pathlib import Path

import yaml

from app.models.assessment import Assessment


class AssessmentLoader:

    def load(self, file_path: str | Path) -> Assessment:

        path = Path(file_path)

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return Assessment(**data)