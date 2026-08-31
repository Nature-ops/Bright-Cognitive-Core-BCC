from pydantic import BaseModel, Field


class Exercise(BaseModel):
    id: str
    title: str
    description: str
    steps: list[str]
    verification: str
    objective_ids: list[str] = Field(default_factory=list)
