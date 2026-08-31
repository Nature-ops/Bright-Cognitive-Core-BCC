from pydantic import BaseModel


class AssessmentRemediation(BaseModel):
    question_id: str
    prompt: str
    explanation: str
