from pydantic import BaseModel, Field

from app.models.question import Question


class Assessment(BaseModel):
    id: str

    title: str

    description: str = ""

    questions: list[Question] = Field(default_factory=list)

    passing_score: int = 70