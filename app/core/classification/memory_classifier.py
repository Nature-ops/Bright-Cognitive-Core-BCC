from app.core.state.cognitive_state import Classification
from app.utils.logger import logger
from app.core.state.cognitive_state import (CognitiveState,Classification,)
from app.core.base.cognitive_engine import CognitiveEngine



  

class MemoryClassifier(CognitiveEngine):

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

    def process(
        self,
        state: CognitiveState
    ) -> CognitiveState:

        text = state.message.lower()

        for memory_type, rule in self.rules.items():

            for keyword in rule["keywords"]:

                if keyword in text:

                    state.classification = Classification(
                        intent="store",
                        memory_type=memory_type,
                        category=rule["category"],
                        importance=rule["importance"],
                        confidence=1.0,
                        action="create",
                        source="rule_engine"
                    )

                    logger.info(
                        f"Classification created: {state.classification.memory_type}"
                        
                    )

                    return state

        # Only return this after ALL rules have been checked.
        state.classification = Classification(
            intent="conversation",
            memory_type="conversation",
            category="general",
            importance="low",
            confidence=1.0,
            action="ignore",
            source="rule_engine"
        )

        logger.info(
            "Classification created: conversation"
            
        )

        return state