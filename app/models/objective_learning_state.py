from typing import Literal

from pydantic import BaseModel


class ObjectiveLearningState(BaseModel):
    """Current interpretation of historical objective assessment evidence."""

    framework_id: str
    objective_id: str
    state: Literal["REPEATED_GAP", "RECOVERY_EVIDENCE"]
    historical_missed_attempt_count: int
    successful_attempt_count_after_last_miss: int
