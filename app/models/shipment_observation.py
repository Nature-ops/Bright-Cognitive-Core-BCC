from pydantic import BaseModel, Field


class ShipmentObservation(BaseModel):
    """A factual shipment ETA observation."""

    shipment_id: str
    expected_arrival_minutes: int = Field(ge=0)
    current_eta_minutes: int = Field(ge=0)
