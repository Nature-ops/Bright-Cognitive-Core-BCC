import logging
from app.core.state.cognitive_state import CognitiveState
from app.core.routing.intent_router import IntentRouter
from app.core.classification.memory_classifier import MemoryClassifier
from app.core.evolution.memory_evolution_engin import MemoryEvolutionEngine
from app.core.context.context_engine import ContextEngine
from app.core.reasoning.reasoning_engine import ReasoningEngine
from app.core.reflection.reflection_engine import ReflectionEngine
from app.core.knowledge.knowledge_engine import KnowledgeEngine
from app.core.planning.planning_engine import PlanningEngine
logger = logging.getLogger(__name__)


class CognitivePipeline:

    def __init__(self):
        self.engines = [

            IntentRouter(),

            MemoryClassifier(),

            MemoryEvolutionEngine(),

            KnowledgeEngine(),

            ReflectionEngine(),

            ContextEngine(),

            PlanningEngine(),

            ReasoningEngine(),

            

         ]

        

    def run(
        self,
        state: CognitiveState
    ) -> CognitiveState:
        
        logger.info("Cognitive Pipeline started.")


        for engine in self.engines:
            state = engine.process(
            state
        )
            
        logger.info("Cognitive Pipeline completed.")   

        return state


        
