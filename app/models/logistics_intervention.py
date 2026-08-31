from typing import Literal

from pydantic import BaseModel


class LogisticsIntervention(BaseModel):
    """A deterministic specification for a logistics activity."""

    shipment_id: str
    intervention_type: Literal[
        "MONITORING",
        "CUSTOMER_NOTIFICATION",
        "DELAY_ESCALATION",
    ]
    required_activity: Literal["OBSERVE", "NOTIFY", "ESCALATE"]
    source_action: Literal["MONITOR", "NOTIFY", "ESCALATE"]
    reason: str
