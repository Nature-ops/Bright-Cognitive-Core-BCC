from app.models.assessment import Assessment
from app.services.assessment_loader import AssessmentLoader
from app.services.base_engine import BaseEngine


class AssessmentEngine(BaseEngine[Assessment]):

    def __init__(self):

        super().__init__(
            AssessmentLoader()
        )

    def get_assessment(
        self,
        assessment_id: str
    ) -> Assessment:

        return self.get(assessment_id)

    def get_assessments(
        self,
    ) -> list[Assessment]:

        return self.get_all()