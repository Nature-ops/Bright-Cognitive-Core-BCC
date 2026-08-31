from app.models.study_session import StudySession
from app.models.study_progress import StudyProgress
from app.models.framework import Framework
from datetime import datetime, UTC 
from app.models.objective import Objective
from app.models.exercise import Exercise
from app.models.assessment_result import AssessmentResult
from app.models.assessment_evidence import AssessmentEvidence
from app.services.assessment_service import AssessmentService
from app.services.assessment_remediation_service import (
    AssessmentRemediationService,
)
from app.services.learning_gap_service import LearningGapService
from app.repositories.json_learning_progress_repository import (
    JsonLearningProgressRepository,
)
from app.repositories.json_study_progress_repository import (
    JsonStudyProgressRepository,
)
from app.repositories.json_assessment_evidence_repository import (
    JsonAssessmentEvidenceRepository,
)
from app.repositories.assessment_evidence_repository import (
    AssessmentEvidenceRepository,
)
from app.repositories.learning_progress_repository import (
    LearningProgressRepository,
)
from app.repositories.study_progress_repository import (
    StudyProgressRepository,
)



class StudyEngine:

    def __init__(
        self,
        framework_progress_repository: LearningProgressRepository | None = None,
        study_progress_repository: StudyProgressRepository | None = None,
        assessment_evidence_repository: AssessmentEvidenceRepository | None = None,
    ):

        self.session: StudySession | None = None

        self.study_progress_repository = (
            study_progress_repository
            or JsonStudyProgressRepository()
        )

        self.progress: StudyProgress | None = None

        self.assessment_evidence_repository = (
            assessment_evidence_repository
            or JsonAssessmentEvidenceRepository()
        )

        self.assessment_service = AssessmentService()

        self.assessment_remediation_service = (
            AssessmentRemediationService()
        )

        self.learning_gap_service = LearningGapService()

        self.framework_progress_service = (
            framework_progress_repository
            or JsonLearningProgressRepository()
        )

        


    def start_session(
        self,
        session: StudySession,
    )-> None:

        self.session = session

        saved_progress = self.study_progress_repository.load(session.id)

        if saved_progress is not None:

            self.progress = saved_progress

        else:

            self.progress = StudyProgress(
                session_id=session.id
            )

            self.progress.updated_at = datetime.now(UTC)

            self.study_progress_repository.save(self.progress)




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


    

            self.study_progress_repository.save(
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


    def current_framework(self) -> Framework | None:
        if self.session is None:
            return None

        return self.session.learning_plan.framework


    def milestone_progress(self) -> float:
        self._require_session()

        framework = self.current_framework()

        assert framework is not None

        milestone_ids = [
            milestone.id
            for milestone in framework.milestones
        ]

        return self.framework_progress_service.milestone_progress(
            framework.id,
            milestone_ids,
        )


    def completed_milestones(self) -> list[str]:
        self._require_session()

        framework = self.current_framework()

        assert framework is not None

        return (
            self.framework_progress_service
            .get_progress(framework.id)
            .completed_milestones
        )


    def is_completed(self) -> bool:

        self._require_session()

        assert self.session is not None
        assert self.progress is not None

        objectives_completed = (
            len(self.progress.completed_objectives)
            == len(self.session.objectives)
        )

        exercises_completed = (
            len(self.progress.completed_exercises)
            == len(self.session.exercises)
        )

        assessment_completed = (
        self.session.assessment is None
        or self.progress.assessment_completed
        )

        return (
            objectives_completed
            and exercises_completed
            and assessment_completed
     )
        


    

    def finish_session(self) -> bool:

        self._require_session()

        completed = self.is_completed()

        if completed:

            assert self.session is not None

            learning_plan = self.session.learning_plan

            self.framework_progress_service.complete_milestone(
                framework_id=learning_plan.framework.id,
                milestone_id=learning_plan.milestone.id,
            )

            self.study_progress_repository.delete(
                self.session.id
            )

        return completed



    def current_exercise(self) -> Exercise | None:

        self._require_session()

        assert self.session is not None
        assert self.progress is not None

        for exercise in self.session.exercises:

            if exercise.id not in self.progress.completed_exercises:

                return exercise

        return None


    def complete_exercise(
        self,
        exercise_id: str,
    ) -> None:

        self._require_session()

        assert self.progress is not None

        if exercise_id not in self.progress.completed_exercises:

            self.progress.completed_exercises.append(
                exercise_id
            )

            self.progress.updated_at = datetime.now(UTC)

            self.study_progress_repository.save(
                self.progress
            )
    

    def get_exercise_progress(self) -> float:

        self._require_session()

        assert self.session is not None
        assert self.progress is not None

        total = len(self.session.exercises)

        completed = len(
            self.progress.completed_exercises
        )

        if total == 0:
            return 100.0

        return completed / total * 100


    def submit_assessment(
        self,
        answers: dict[str, str],
    ) -> AssessmentResult:

        self._require_session()

        assert self.session is not None
        assert self.progress is not None

        assessment = self.session.assessment

        if assessment is None:
            raise RuntimeError(
                "This study session has no assessment."
            )

        result = self.assessment_service.evaluate(
            assessment,
            answers,
        )

        result.remediation = (
            self.assessment_remediation_service
            .create_remediation(assessment, result)
        )

        result.learning_gaps = (
            self.learning_gap_service.create_learning_gaps(
                assessment,
                result,
            )
        )

        self.assessment_evidence_repository.record_attempt(
            AssessmentEvidence(
                framework_id=(
                    self.session.learning_plan.framework.id
                ),
                milestone_id=(
                    self.session.learning_plan.milestone.id
                ),
                assessment_id=result.assessment_id,
                score=result.score,
                passed=result.passed,
                incorrect_question_ids=result.incorrect_question_ids,
                learning_gap_objective_ids=[
                    gap.objective_id
                    for gap in result.learning_gaps
                ],
            )
        )

        if result.passed:

            self.progress.assessment_completed = True

            self.progress.updated_at = datetime.now(UTC)

            self.study_progress_repository.save(
                self.progress
            )

        return result


    def current_assessment(self):

        self._require_session()

        assert self.session is not None

        return self.session.assessment
