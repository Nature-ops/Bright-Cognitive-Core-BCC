from pydantic import BaseModel, Field


class Question(BaseModel):
    id: str

    prompt: str

    options: list[str] = Field(default_factory=list)

    answer: str

    explanation: str = ""