from unittest import TestCase

from pydantic import ValidationError

from app.models.intervention_outcome_evidence import (
    InterventionOutcomeEvidence,
)
from app.models.logistics_outcome import LogisticsOutcome


class CompletionStatusContractTest(TestCase):
    def test_outcome_models_accept_shared_completion_statuses(self):
        for completion_status in ("COMPLETED", "NOT_COMPLETED"):
            with self.subTest(completion_status=completion_status):
                learning_outcome = InterventionOutcomeEvidence(
                    framework_id="aws-sa",
                    objective_id="iam-users",
                    intervention_type="REINFORCEMENT",
                    required_activity="PRACTICE",
                    completion_status=completion_status,
                    source_action="REINFORCE_OBJECTIVE",
                )
                logistics_outcome = LogisticsOutcome(
                    shipment_id="shipment-42",
                    intervention_type="MONITORING",
                    required_activity="OBSERVE",
                    source_action="MONITOR",
                    completion_status=completion_status,
                )

                self.assertEqual(
                    learning_outcome.completion_status,
                    completion_status,
                )
                self.assertEqual(
                    logistics_outcome.completion_status,
                    completion_status,
                )

    def test_outcome_models_reject_invalid_completion_status(self):
        with self.assertRaises(ValidationError):
            InterventionOutcomeEvidence(
                framework_id="aws-sa",
                objective_id="iam-users",
                intervention_type="REINFORCEMENT",
                required_activity="PRACTICE",
                completion_status="SUCCEEDED",
                source_action="REINFORCE_OBJECTIVE",
            )

        with self.assertRaises(ValidationError):
            LogisticsOutcome(
                shipment_id="shipment-42",
                intervention_type="MONITORING",
                required_activity="OBSERVE",
                source_action="MONITOR",
                completion_status="SUCCEEDED",
            )
