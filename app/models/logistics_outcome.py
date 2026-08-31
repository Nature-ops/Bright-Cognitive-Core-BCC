from typing import Literal

from pydantic import BaseModel

from app.core.cognitive.completion_status import CompletionStatus


class LogisticsOutcome(BaseModel):
    """A factual record of whether the requested logistics activity occurred."""

    shipment_id: str
    intervention_type: Literal[
        "MONITORING",
        "CUSTOMER_NOTIFICATION",
        "DELAY_ESCALATION",
    ]
    required_activity: Literal["OBSERVE", "NOTIFY", "ESCALATE"]
    source_action: Literal["MONITOR", "NOTIFY", "ESCALATE"]
    completion_status: CompletionStatus
