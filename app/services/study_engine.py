from app.models.study_session import StudySession
from app.models.study_progress import StudyProgress
from datetime import datetime, UTC 
from app.models.objective import Objective
from app.services.study_progress_service import StudyProgressService



class StudyEngine:

    def __init__(self):

        self.session: StudySession | None = None

        self.progress_service = StudyProgressService()

        self.progress: StudyProgress | None = None

        


    def start_session(
        self,
        session: StudySession,
    )-> None:

        self.session = session

        saved_progress = self.progress_service.load(session.id)

        if saved_progress is not None:

            self.progress = saved_progress

        else:

            self.progress = StudyProgress(
                session_id=session.id
            )

            self.progress.updated_at = datetime.now(UTC)

            self.progress_service.save(self.progress)




    def current_objective(self) -> Objective | None:

        self._require_session()

        assert self.session is not None

    
        assert self.progress is not None

        for objective in self.session.objectives:

            if objective.id not in self.progress.completed_objectives:

                return objective
        return None


    def _require_session(self) -> None:

        if self.session is None:
            raise RuntimeError(
            "No study session has been started."
        )
    
    
    def complete_objective(
        self,
        objective_id: str,
    ) -> None:
        self._require_session()


        assert self.progress is not None


        if objective_id not in self.progress.completed_objectives:

            self.progress.completed_objectives.append(objective_id)

            self.progress.updated_at = datetime.now(UTC)


    

            self.progress_service.save(
                self.progress
            )




    def get_progress(self) -> float:

        self._require_session()

        assert self.session is not None

        assert self.progress is not None

        total = len(self.session.objectives)

        completed = len(self.progress.completed_objectives)

        if total == 0:

            return 100.0

        return completed / total * 100        


    def is_completed(self) -> bool:

        self._require_session()

        assert self.session is not None

        assert self.progress is not None

        return len(
            self.progress.completed_objectives
        ) == len(self.
            session.objectives
        )


    

    def finish_session(self) -> bool:

        self._require_session()

        completed = self.is_completed()

        if completed:

            assert self.session is not None

            self.progress_service.delete(
                self.session.id
            )

        return completed