from typing import Literal

from pydantic import BaseModel


class LogisticsDecision(BaseModel):
    """A deterministic operational decision for a shipment delay state."""

    shipment_id: str
    action: Literal["MONITOR", "NOTIFY", "ESCALATE"]
    reason: str
    source_state: Literal["ON_TIME", "DELAY_RISK", "DELAYED"]
