from unittest import TestCase

from app.models.logistics_outcome import LogisticsOutcome
from app.models.shipment_observation import ShipmentObservation
from app.services.logistics_decision_service import LogisticsDecisionService
from app.services.logistics_feedback_service import LogisticsFeedbackService
from app.services.logistics_intervention_service import (
    LogisticsInterventionService,
)
from app.services.shipment_delay_state_service import (
    ShipmentDelayStateService,
)


class LogisticsDelayIntelligenceTest(TestCase):
    def setUp(self):
        self.delay_state_service = ShipmentDelayStateService()
        self.decision_service = LogisticsDecisionService()
        self.intervention_service = LogisticsInterventionService()
        self.feedback_service = LogisticsFeedbackService()

    def pipeline(self, expected: int, current: int):
        observation = ShipmentObservation(
            shipment_id="shipment-42",
            expected_arrival_minutes=expected,
            current_eta_minutes=current,
        )
        delay_state = self.delay_state_service.create_delay_state(
            observation
        )
        decision = self.decision_service.create_decision(delay_state)
        intervention = self.intervention_service.create_intervention(decision)
        return observation, delay_state, decision, intervention

    def outcome(self, intervention, completion_status: str) -> LogisticsOutcome:
        return LogisticsOutcome(
            shipment_id=intervention.shipment_id,
            intervention_type=intervention.intervention_type,
            required_activity=intervention.required_activity,
            source_action=intervention.source_action,
            completion_status=completion_status,
        )

    def test_delay_thresholds_include_negative_and_boundaries(self):
        cases = [
            (100, 95, "ON_TIME", -5),
            (100, 105, "ON_TIME", 5),
            (100, 106, "DELAY_RISK", 6),
            (100, 115, "DELAY_RISK", 15),
            (100, 116, "DELAYED", 16),
        ]

        for expected, current, expected_state, delay in cases:
            with self.subTest(delay=delay):
                _, state, _, _ = self.pipeline(expected, current)
                self.assertEqual(state.state, expected_state)
                self.assertEqual(state.delay_minutes, delay)

    def test_state_decisions_have_fixed_actions_and_reasons(self):
        cases = [
            (
                105,
                "MONITOR",
                "Shipment remains within the acceptable arrival window.",
            ),
            (
                106,
                "NOTIFY",
                "Shipment delay risk requires proactive notification.",
            ),
            (
                116,
                "ESCALATE",
                "Shipment delay exceeds the acceptable threshold and "
                "requires escalation.",
            ),
        ]

        for current, action, reason in cases:
            with self.subTest(action=action):
                _, state, decision, _ = self.pipeline(100, current)
                self.assertEqual(decision.action, action)
                self.assertEqual(decision.reason, reason)
                self.assertEqual(decision.source_state, state.state)

    def test_decisions_create_fixed_interventions_and_reasons(self):
        cases = [
            (
                105,
                "MONITORING",
                "OBSERVE",
                "Continue observing the shipment for ETA changes.",
            ),
            (
                106,
                "CUSTOMER_NOTIFICATION",
                "NOTIFY",
                "Notify the affected party about the developing shipment "
                "delay.",
            ),
            (
                116,
                "DELAY_ESCALATION",
                "ESCALATE",
                "Escalate the shipment delay for operational intervention.",
            ),
        ]

        for current, intervention_type, activity, reason in cases:
            with self.subTest(intervention_type=intervention_type):
                _, _, decision, intervention = self.pipeline(100, current)
                self.assertEqual(
                    intervention.intervention_type,
                    intervention_type,
                )
                self.assertEqual(intervention.required_activity, activity)
                self.assertEqual(intervention.source_action, decision.action)
                self.assertEqual(intervention.reason, reason)

    def test_not_completed_activity_requires_retry(self):
        _, _, _, intervention = self.pipeline(100, 116)

        feedback = self.feedback_service.create_feedback(
            intervention,
            self.outcome(intervention, "NOT_COMPLETED"),
        )

        self.assertEqual(feedback.feedback_state, "RETRY_INTERVENTION")
        self.assertEqual(
            feedback.reason,
            "The requested logistics activity was not completed and "
            "should be retried.",
        )

    def test_completed_interventions_require_the_specified_follow_up(self):
        cases = [
            (
                105,
                "CONTINUE_MONITORING",
                "Monitoring was completed; continue observing for updated "
                "shipment conditions.",
            ),
            (
                106,
                "AWAIT_NEW_OBSERVATION",
                "Notification was completed; new shipment evidence is "
                "required before further action.",
            ),
            (
                116,
                "AWAIT_NEW_OBSERVATION",
                "Escalation was completed; new shipment evidence is "
                "required before evaluating the delay again.",
            ),
        ]

        for current, feedback_state, reason in cases:
            with self.subTest(feedback_state=feedback_state):
                _, _, _, intervention = self.pipeline(100, current)
                feedback = self.feedback_service.create_feedback(
                    intervention,
                    self.outcome(intervention, "COMPLETED"),
                )
                self.assertEqual(feedback.feedback_state, feedback_state)
                self.assertEqual(feedback.reason, reason)

    def test_mismatched_outcome_fails_explicitly(self):
        _, _, _, intervention = self.pipeline(100, 116)
        mismatched = LogisticsOutcome(
            shipment_id="different-shipment",
            intervention_type=intervention.intervention_type,
            required_activity=intervention.required_activity,
            source_action=intervention.source_action,
            completion_status="COMPLETED",
        )

        with self.assertRaisesRegex(
            ValueError,
            "Logistics outcome does not match the source intervention.",
        ):
            self.feedback_service.create_feedback(intervention, mismatched)

    def test_full_vertical_scenarios_preserve_shipment_and_inputs(self):
        cases = [
            (105, "MONITOR", "MONITORING", "CONTINUE_MONITORING"),
            (106, "NOTIFY", "CUSTOMER_NOTIFICATION", "AWAIT_NEW_OBSERVATION"),
            (116, "ESCALATE", "DELAY_ESCALATION", "AWAIT_NEW_OBSERVATION"),
        ]

        for current, action, intervention_type, feedback_state in cases:
            with self.subTest(action=action):
                observation, state, decision, intervention = self.pipeline(
                    100,
                    current,
                )
                outcome = self.outcome(intervention, "COMPLETED")
                original_observation = observation.model_dump()
                original_state = state.model_dump()
                original_decision = decision.model_dump()
                original_intervention = intervention.model_dump()
                original_outcome = outcome.model_dump()

                feedback = self.feedback_service.create_feedback(
                    intervention,
                    outcome,
                )

                self.assertEqual(decision.action, action)
                self.assertEqual(intervention.intervention_type, intervention_type)
                self.assertEqual(feedback.feedback_state, feedback_state)
                self.assertEqual(feedback.shipment_id, "shipment-42")
                self.assertEqual(observation.model_dump(), original_observation)
                self.assertEqual(state.model_dump(), original_state)
                self.assertEqual(decision.model_dump(), original_decision)
                self.assertEqual(intervention.model_dump(), original_intervention)
                self.assertEqual(outcome.model_dump(), original_outcome)
