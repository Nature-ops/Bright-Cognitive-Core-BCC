class MemoryClassifier:

    def __init__(self):

        self.rules = {
            "fact": {
                "keywords": [
                    "my name is",
                    "i live in",
                    "i work as"
                ],
                "category": "identity",
                "importance": "high"
            },

            "learning": {
                "keywords": [
                    "i am studying",
                    "i'm studying",
                    "i am learning",
                    "i'm learning",
                    "i learned"
                ],
                "category": "education",
                "importance": "high"
            },

            "goal": {
                "keywords": [
                    "i want to",
                    "my goal is",
                    "i plan to"
                ],
                "category": "personal",
                "importance": "high"
            },

            "project": {
                "keywords": [
                    "i am building",
                    "i'm building",
                    "i am working on",
                    "i'm working on"
                ],
                "category": "development",
                "importance": "high"
            },

            "preference": {
                "keywords": [
                    "i prefer",
                    "my favorite",
                    "i like",
                    "i enjoy"
                ],
                "category": "personal",
                "importance": "medium"
            },

            "task": {
                "keywords": [
                    "remind me",
                    "i need to",
                    "i have to",
                    "todo",
                    "to-do"
                ],
                "category": "productivity",
                "importance": "medium"
            }
        }

    def classify(self, message: str) -> dict:

        text = message.lower()

        for memory_type, rule in self.rules.items():

            for keyword in rule["keywords"]:

                if keyword in text:

                    return {
                        "intent": "store",
                        "memory_type": memory_type,
                        "category": rule["category"],
                        "importance": rule["importance"],
                        "confidence": 1.0,
                        "action": "create"
                    }

        return {
            "intent": "conversation",
            "memory_type": "conversation",
            "category": "general",
            "importance": "low",
            "confidence": 1.0,
            "action": "ignore"
        }