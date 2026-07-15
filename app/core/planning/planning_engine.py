from app.core.base.cognitive_engine import CognitiveEngine
from app.core.state.cognitive_state import (
    CognitiveState,
    Plan,
)
from app.utils.logger import logger


class PlanningEngine(CognitiveEngine):

    def process(
        self,
        state: CognitiveState
    ) -> CognitiveState:

        if state.intent != "learning" or state.context is None:
            return state

        state.plan = Plan(
            title="Learning Plan",
            steps=[
                "Review your previous study session.",
                "Complete one focused learning session.",
                "Record what you learned today.",
            ],
        )

        logger.info(
            "Planning: learning plan created."
        )

        return state