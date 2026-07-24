from pydantic import BaseModel


class Exercise(BaseModel):
    id: str
    title: str
    description: str
    steps: list[str]
    verification: str