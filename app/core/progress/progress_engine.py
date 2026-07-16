
from app.core.base.cognitive_engine import CognitiveEngine
from app.core.state.cognitive_state import (CognitiveState,GoalProgress,)
from app.utils.logger import logger


class ProgressEngine(CognitiveEngine):
     
     def process(
        self,
        state: CognitiveState
    ) -> CognitiveState:
        
        if state.goal is None:
                return state

        if state.context is None:
            return state
        
        knowledge = state.context.knowledge
        learning = knowledge.get("Learning", [])

        completed = [
             item["content"]
             for item in learning
        ]

        
        progress = 100.0 if completed else 0.0
        
        remaining = []

        state.goal_progress = GoalProgress(
                goal=state.goal.title,
                progress=progress,
                completed=completed,
                remaining=remaining,
            )
        

        logger.info(
             f"Goal progress: {progress}%"
        )
            


        return state