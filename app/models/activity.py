from enum import Enum
from pydantic import BaseModel


class ActivityType(str, Enum):
    OBJECTIVE = "objective"
    EXERCISE = "exercise"
    ASSESSMENT = "assessment"
    COMPLETED = "completed"


class Activity(BaseModel):
    type: ActivityType
    item: object | None = None


