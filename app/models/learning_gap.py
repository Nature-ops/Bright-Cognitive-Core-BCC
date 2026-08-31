from pydantic import BaseModel, Field


class LearningGap(BaseModel):
    objective_id: str
    reason: str
    source_question_ids: list[str] = Field(default_factory=list)
