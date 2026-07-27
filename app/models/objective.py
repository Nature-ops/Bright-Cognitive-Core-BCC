from pydantic import BaseModel


class Objective(BaseModel):
    id: str
    title: str
    completed: bool = False