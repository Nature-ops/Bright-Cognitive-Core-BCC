from typing import Literal

from pydantic import BaseModel


class LearningDecision(BaseModel):
    """A deterministic learning action derived from current objective state."""

    framework_id: str
    objective_id: str
    action: Literal["REINFORCE_OBJECTIVE", "VERIFY_RECOVERY"]
    reason: str
    source_state: Literal["REPEATED_GAP", "RECOVERY_EVIDENCE"]
