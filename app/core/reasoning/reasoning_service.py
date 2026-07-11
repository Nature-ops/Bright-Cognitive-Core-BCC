class ReasoningService:

    def summarize_user(self, knowledge: dict) -> str:

        lines = [
            "Here's what I know about you.",
            ""
        ]

        for title, items in knowledge.items():

            if not items:
                continue

            lines.append(f"{title}:")

            for item in items:

                if isinstance(item, dict):
                    lines.append(f"- {item['content']}")
                else:
                    lines.append(f"- {item}")

            lines.append("")

        return "\n".join(lines)

    def recommend_learning(self, knowledge: dict) -> str:

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

        return "\n".join(lines)

    def recommend_tasks(self, knowledge: dict) -> str:

        tasks = knowledge.get("Tasks", [])

        if not tasks:
            return (
                "You don't have any recorded tasks."
            )

        lines = [
            "Your current tasks:",
            ""
        ]

        for task in tasks:
            lines.append(f"- {task['content']}")

        return "\n".join(lines)