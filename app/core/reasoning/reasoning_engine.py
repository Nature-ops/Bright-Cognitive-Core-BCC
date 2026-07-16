from app.core.base.cognitive_engine import CognitiveEngine
from app.core.state.cognitive_state import (
    CognitiveState,
    Response,
)


class ReasoningEngine(CognitiveEngine):

    def process(
        self,
        state: CognitiveState,
    ) -> CognitiveState:

        if state.context is None:
            return state

        if state.intent == "learning":
            message = self.recommend_learning(state)

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

    # -------------------------------------------------
    # Knowledge Summary
    # -------------------------------------------------

    def summarize_user(
        self,
        context: dict,
    ) -> str:

        lines = [
            "Here's what I know about you.",
            "",
        ]

        for title, items in context.items():

            if not items:
                continue

            lines.append(f"{title}:")

            for item in items:

                if isinstance(item, dict):
                    lines.append(
                        f"- {item['content']}"
                    )

                else:
                    lines.append(f"- {item}")

            lines.append("")

        return "\n".join(lines)

    # -------------------------------------------------
    # Learning Recommendation
    # -------------------------------------------------

    def recommend_learning(
        self,
        state: CognitiveState,
    ) -> str:
        context = state.context

        if context is None:
             return "No context available."

        knowledge = context.knowledge

        learning = knowledge.get(
            "Learning",
            [],
        )

        goals = knowledge.get(
            "Goals",
            [],
        )

        if not learning:
            return (
                "I don't know what you're studying yet."
            )

        lines = [
            "Based on what I know about you:",
            "",
        ]

        # ---------------------------------------------
        # Goals
        # ---------------------------------------------

        if goals:

            lines.append(
                "Your learning supports these goals:"
            )

            for goal in goals:
                lines.append(
                    f"- {goal['content']}"
                )

            lines.append("")

        # ---------------------------------------------
        # Goal Progress
        # ---------------------------------------------

        goal_progress = state.goal_progress

        if goal_progress:

            lines.append("Goal Progress:")
            lines.append(
                f"- Goal: {goal_progress.goal}"
            )
            lines.append(
                f"- Progress: {goal_progress.progress:.0f}%"
            )
            lines.append("")

            if goal_progress.completed:

                lines.append(
                    "Completed Learning:"
                )

                for item in goal_progress.completed:
                    lines.append(f"✓ {item}")

                lines.append("")

        # ---------------------------------------------
        # Recommendation
        # ---------------------------------------------

        if goal_progress:

            if goal_progress.progress >= 100:

                lines.append(
                    "Recommendation:"
                )
                lines.append(
                    "You're ready to move to the next milestone."
                )

            else:

                lines.append(
                    "Recommendation:"
                )
                lines.append(
                    "Continue progressing toward your current goal."
                )

            lines.append("")

        # ---------------------------------------------
        # Plan
        # ---------------------------------------------

        if state.plan:

            lines.append(
                "Recommended Next Steps:"
            )

            for step in state.plan.steps:
                lines.append(f"- {step}")

            lines.append("")

        return "\n".join(lines)

    # -------------------------------------------------
    # Task Recommendation
    # -------------------------------------------------

    def recommend_tasks(
        self,
        context: dict,
    ) -> str:

        tasks = context.get(
            "Tasks",
            [],
        )

        if not tasks:
            return (
                "You don't have any recorded tasks."
            )

        lines = [
            "Your current tasks:",
            "",
        ]

        for task in tasks:
            lines.append(
                f"- {task['content']}"
            )

        return "\n".join(lines)