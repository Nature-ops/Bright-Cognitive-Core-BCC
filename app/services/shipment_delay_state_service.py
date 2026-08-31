from app.models.shipment_delay_state import ShipmentDelayState
from app.models.shipment_observation import ShipmentObservation


class ShipmentDelayStateService:
    """Interpret a shipment ETA observation using fixed delay thresholds."""

    def create_delay_state(
        self,
        observation: ShipmentObservation,
    ) -> ShipmentDelayState:
        delay_minutes = (
            observation.current_eta_minutes
            - observation.expected_arrival_minutes
        )

        if delay_minutes <= 5:
            state = "ON_TIME"
        elif delay_minutes <= 15:
            state = "DELAY_RISK"
        else:
            state = "DELAYED"

        return ShipmentDelayState(
            shipment_id=observation.shipment_id,
            state=state,
            delay_minutes=delay_minutes,
        )
