from app.models.logistics_decision import LogisticsDecision
from app.models.shipment_delay_state import ShipmentDelayState


class LogisticsDecisionService:
    """Map a shipment delay state to a deterministic operational action."""

    def create_decision(
        self,
        delay_state: ShipmentDelayState,
    ) -> LogisticsDecision:
        if delay_state.state == "ON_TIME":
            action = "MONITOR"
            reason = "Shipment remains within the acceptable arrival window."
        elif delay_state.state == "DELAY_RISK":
            action = "NOTIFY"
            reason = "Shipment delay risk requires proactive notification."
        else:
            action = "ESCALATE"
            reason = (
                "Shipment delay exceeds the acceptable threshold and "
                "requires escalation."
            )

        return LogisticsDecision(
            shipment_id=delay_state.shipment_id,
            action=action,
            reason=reason,
            source_state=delay_state.state,
        )
