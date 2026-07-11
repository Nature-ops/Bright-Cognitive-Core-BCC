class MemoryEvolutionEngine:

    def evolve(
        self,
        classification: dict,
        message: str
    ) -> dict:

        text = message.lower()

        if (
            "i passed" in text
            or "i completed" in text
            or "i finished" in text
        ):

            classification["intent"] = "store"
            classification["memory_type"] = "achievement"
            classification["action"] = "create"

        return classification