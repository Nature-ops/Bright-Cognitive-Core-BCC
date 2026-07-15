from abc import ABC, abstractmethod


from app.core.state.cognitive_state import CognitiveState


class CognitiveEngine(ABC):


    @abstractmethod
    def process(
        self,
        state: CognitiveState
    ) -> CognitiveState:
        """
        process the cognitive state and return it.
        """
        pass

    