from app.core.base.cognitive_engine import CognitiveEngine
from app.core.state.cognitive_state import (CognitiveState,Plan,)
from app.core.planning.planning_rules import RULES
from app.utils.logger import logger


class PlanningEngine(CognitiveEngine):

    def process(
        self,
        state: CognitiveState
    ) -> CognitiveState:

        if state.intent != "learning" or state.context is None:
            return state
        
        knowledge = state.context.knowledge
        learning = knowledge.get("Learning", [])

        goal_title = "General Learning"

        if state.priority:
            goal_title = state.priority.title


        steps = []

        for item in learning:

            text = item["content"].lower()

            for topic, topic_steps in RULES.items():

                if topic in text:

                    steps.extend(topic_steps)




        if not steps:

            steps = [
                "Continue your current learning journey."
            ]

        # Remove duplicate steps while preserving order
        steps = list(dict.fromkeys(steps))
            
        state.plan = Plan(
            title=f"Plan for: {goal_title}",
            steps=steps,
        )

        logger.info(
            "Planning: learning plan created."
        )



        

        return state