from app.core.state.cognitive_state import (CognitiveState,Response,)
from app.core.base.cognitive_engine import CognitiveEngine



class ReasoningEngine(CognitiveEngine):

    def process(
        self,
        state: CognitiveState
        ) -> CognitiveState:


        if state.context is None:
            return state

        if state.intent == "learning":

            message = self.recommend_learning(
                state

            )

        elif state.intent == "knowledge_summary":

            message = self.summarize_user(
                state.context.knowledge
            )
            
        else:
            return state

        state.response = Response(
            message=message
        )

        return state



    def summarize_user(self, context: dict) -> str:

        lines = [
            "Here's what I know about you.",
            ""
        ]

        for title, items in context.items():

            if not items:
                continue

            lines.append(f"{title}:")

            for item in items:

                if isinstance(item, dict):
                    lines.append(f"- {item['content']}")
                else:
                    lines.append(f"- {item}")

            


        return "\n".join(lines)
        


    def recommend_learning(
            self,
            state: CognitiveState
        ) -> str:

        context = state.context
        knowledge = getattr(context, "knowledge", {}) or {}

        learning = knowledge.get("Learning", [])
        goals = knowledge.get("Goals", [])

        if not learning:
            return (
                "I don't know what you're studying yet."
            )

        lines = [
            "Based on what I know about you:",
            ""
        ]

        if goals:
            lines.append(
                "Your learning supports these goals:"
            )

            for goal in goals:
                lines.append(f"- {goal['content']}")

            lines.append("")

        lines.append("Current learning:")

        for item in learning:
            lines.append(f"- {item['content']}")

        lines.append("")
        lines.append(
            "Recommendation: Continue building consistent progress before moving to a new topic."
        )

        
        if state.plan:

            lines.append("")
            lines.append("Recommended Next Steps:")

            for step in state.plan.steps:
                lines.append(f"- {step}")  

        return "\n".join(lines)

    def recommend_tasks(self, context: dict) -> str:

        tasks = context.get("Tasks", [])

        if not tasks:
            return (
                "You don't have any recorded tasks."
            )

        lines = [
            "Your current tasks:",
            ""
        ]

         

        return "\n".join(lines)