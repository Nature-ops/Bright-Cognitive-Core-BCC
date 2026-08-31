from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


class InterventionOutcomeEvidence(BaseModel):
    """An append-only factual record of an intervention activity outcome."""

    framework_id: str
    objective_id: str
    intervention_type: Literal[
        "REINFORCEMENT",
        "RECOVERY_VERIFICATION",
    ]
    required_activity: Literal["PRACTICE", "ASSESSMENT"]
    completion_status: Literal["COMPLETED", "NOT_COMPLETED"]
    source_action: Literal[
        "REINFORCE_OBJECTIVE",
        "VERIFY_RECOVERY",
    ]
    recorded_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
