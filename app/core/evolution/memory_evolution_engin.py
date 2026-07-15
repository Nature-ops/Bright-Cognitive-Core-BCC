from app.core.state.cognitive_state import CognitiveState
from app.utils.logger import logger
from app.core.base.cognitive_engine import CognitiveEngine

class MemoryEvolutionEngine(CognitiveEngine):

    def process(
        self,
        state: CognitiveState
    ) -> CognitiveState:

        text = state.message.lower()

        if state.classification is None:
            return state

        if (
            "i passed" in text
            or "i completed" in text
            or "i finished" in text
        ):

            state.classification.intent = "store"
            state.classification.memory_type = "achievement"
            state.classification.action = "create"

            logger.info(
                "Evolution: learning achievement detected."
            )

        return state