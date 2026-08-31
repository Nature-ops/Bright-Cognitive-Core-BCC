from app.models.logistics_decision import LogisticsDecision
from app.models.logistics_intervention import LogisticsIntervention


class LogisticsInterventionService:
    """Translate a logistics decision into a required operational activity."""

    def create_intervention(
        self,
        decision: LogisticsDecision,
    ) -> LogisticsIntervention:
        if decision.action == "MONITOR":
            intervention_type = "MONITORING"
            required_activity = "OBSERVE"
            reason = "Continue observing the shipment for ETA changes."
        elif decision.action == "NOTIFY":
            intervention_type = "CUSTOMER_NOTIFICATION"
            required_activity = "NOTIFY"
            reason = (
                "Notify the affected party about the developing shipment "
                "delay."
            )
        else:
            intervention_type = "DELAY_ESCALATION"
            required_activity = "ESCALATE"
            reason = (
                "Escalate the shipment delay for operational intervention."
            )

        return LogisticsIntervention(
            shipment_id=decision.shipment_id,
            intervention_type=intervention_type,
            required_activity=required_activity,
            source_action=decision.action,
            reason=reason,
        )
