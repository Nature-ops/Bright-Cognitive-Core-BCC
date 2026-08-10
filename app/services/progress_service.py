import json
from json import JSONDecodeError
from pathlib import Path
from datetime import UTC, datetime
from app.models.progress import Progress



class ProgressService:

    def __init__(self):
        self.progress_file = Path("data/progress.json")

        if not self.progress_file.exists():
            self.progress_file.write_text("[]", encoding="utf-8")

    def load(self) -> list[Progress]:
        try:
            with self.progress_file.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            return [
                Progress.model_validate(item)
                for item in data
            ]

        except (JSONDecodeError, FileNotFoundError):
            return []

    def save(self, records: list[Progress]) -> None:

        data = [
            record.model_dump(mode="json")
            for record in records
        ]

        with self.progress_file.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )


    def get_progress(self, framework_id: str) -> Progress:

        records = self.load()

        for record in records:
            if record.framework_id == framework_id:
                return record

        progress = Progress(
            framework_id=framework_id
        )

        records.append(progress)

        self.save(records)

        return progress


    def update_progress(
        self,
        progress: Progress
    ) -> None:

        records = self.load()

        for index, record in enumerate(records):
            if record.framework_id == progress.framework_id:
                records[index] = progress
                break
        else:
            records.append(progress)

        self.save(records)

    def complete_milestone(
        self,
        framework_id: str,
        milestone_id: str
    ) -> None:

        progress = self.get_progress(framework_id)

        if milestone_id not in progress.completed_milestones:
            progress.completed_milestones.append(
            milestone_id
            )

        progress.updated_at = datetime.now(UTC)

        self.update_progress(progress)



    def milestone_progress(
        self,
        framework_id: str,
        milestone_ids: list[str],
    ) -> float:

        progress = self.get_progress(framework_id)

        total = len(milestone_ids)

        if total == 0:
            return 100.0

        completed = sum(
            1
            for milestone_id in milestone_ids
            if milestone_id in progress.completed_milestones
        )

        return completed / total * 100


