from typing import Literal

from pydantic import BaseModel


class ShipmentDelayState(BaseModel):
    """The deterministic delay state derived from one ETA observation."""

    shipment_id: str
    state: Literal["ON_TIME", "DELAY_RISK", "DELAYED"]
    delay_minutes: int
