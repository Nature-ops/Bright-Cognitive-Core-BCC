from app.models.logistics_feedback import LogisticsFeedback
from app.models.logistics_intervention import LogisticsIntervention
from app.models.logistics_outcome import LogisticsOutcome


class LogisticsFeedbackService:
    """Interpret a matching logistics activity outcome without changing state."""

    def create_feedback(
        self,
        intervention: LogisticsIntervention,
        outcome: LogisticsOutcome,
    ) -> LogisticsFeedback:
        self._validate_identity(intervention, outcome)

        if outcome.completion_status == "NOT_COMPLETED":
            feedback_state = "RETRY_INTERVENTION"
            reason = (
                "The requested logistics activity was not completed and "
                "should be retried."
            )
        elif intervention.intervention_type == "MONITORING":
            feedback_state = "CONTINUE_MONITORING"
            reason = (
                "Monitoring was completed; continue observing for updated "
                "shipment conditions."
            )
        elif intervention.intervention_type == "CUSTOMER_NOTIFICATION":
            feedback_state = "AWAIT_NEW_OBSERVATION"
            reason = (
                "Notification was completed; new shipment evidence is "
                "required before further action."
            )
        else:
            feedback_state = "AWAIT_NEW_OBSERVATION"
            reason = (
                "Escalation was completed; new shipment evidence is "
                "required before evaluating the delay again."
            )

        return LogisticsFeedback(
            shipment_id=intervention.shipment_id,
            source_intervention_type=intervention.intervention_type,
            source_completion_status=outcome.completion_status,
            feedback_state=feedback_state,
            reason=reason,
        )

    def _validate_identity(
        self,
        intervention: LogisticsIntervention,
        outcome: LogisticsOutcome,
    ) -> None:
        if (
            intervention.shipment_id != outcome.shipment_id
            or intervention.intervention_type != outcome.intervention_type
            or intervention.required_activity != outcome.required_activity
            or intervention.source_action != outcome.source_action
        ):
            raise ValueError(
                "Logistics outcome does not match the source intervention."
            )
