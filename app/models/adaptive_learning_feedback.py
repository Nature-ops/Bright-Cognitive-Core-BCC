from typing import Literal

from pydantic import BaseModel


class AdaptiveLearningFeedback(BaseModel):
    """A deterministic interpretation of an intervention outcome."""

    framework_id: str
    objective_id: str
    source_intervention_type: Literal[
        "REINFORCEMENT",
        "RECOVERY_VERIFICATION",
    ]
    source_completion_status: Literal["COMPLETED", "NOT_COMPLETED"]
    feedback_state: Literal[
        "REPEAT_INTERVENTION",
        "READY_FOR_VERIFICATION",
        "AWAITING_ASSESSMENT_EVIDENCE",
    ]
    reason: str
