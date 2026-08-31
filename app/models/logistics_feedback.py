from typing import Literal

from pydantic import BaseModel


class LogisticsFeedback(BaseModel):
    """A deterministic interpretation of one logistics activity outcome."""

    shipment_id: str
    source_intervention_type: Literal[
        "MONITORING",
        "CUSTOMER_NOTIFICATION",
        "DELAY_ESCALATION",
    ]
    source_completion_status: Literal["COMPLETED", "NOT_COMPLETED"]
    feedback_state: Literal[
        "CONTINUE_MONITORING",
        "RETRY_INTERVENTION",
        "AWAIT_NEW_OBSERVATION",
    ]
    reason: str
