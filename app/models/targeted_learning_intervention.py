from typing import Literal

from pydantic import BaseModel


class TargetedLearningIntervention(BaseModel):
    """A deterministic specification for a future learning intervention."""

    framework_id: str
    objective_id: str
    intervention_type: Literal[
        "REINFORCEMENT",
        "RECOVERY_VERIFICATION",
    ]
    reason: str
    source_action: Literal[
        "REINFORCE_OBJECTIVE",
        "VERIFY_RECOVERY",
    ]
    required_activity: Literal["PRACTICE", "ASSESSMENT"]
