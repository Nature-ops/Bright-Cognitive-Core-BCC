
from app.services.ai.ollama_provider import OllamaProvider
from app.services.prompt_service import PromptService
from app.services.memory_service import MemoryService
from app.utils.logger import logger
from app.services.conversation_service import ConversationService
from app.core.classification.memory_classifier import MemoryClassifier
from app.services.knowledge_service import KnowledgeService
from app.core.reasoning.reasoning_service import ReasoningService
from app.core.evolution.memory_evolution_engin import MemoryEvolutionEngine



class ChatService:
    def __init__(self):
        self.provider = OllamaProvider()
        self.knowledge_service = KnowledgeService()
        self.prompt_service = PromptService()
        self.memory = MemoryService()
        self.conversation = ConversationService()
        self.classifier = MemoryClassifier()
        self.reasoning = ReasoningService()
        self.evolution = MemoryEvolutionEngine()



    def chat(self, message: str) -> str:
        

        logger.info(f"Received message: {message}")

        # Step 1: Classify the message
        classification = self.classifier.classify(message)

        logger.info(
            f"Message classified as: {classification}"
        )

        # Step 2: Allow the Evolution Engine to modify the decision
        classification = self.evolution.evolve(
        classification,
        message
        )

        logger.info(
            f"Memory evolution: {classification}"
        )

        # Step 3: Store the memory if needed
        if classification["intent"] == "store":

            self.knowledge_service.process_memory(
            classification,
            message
            )

        logger.info("Knowledge stored successfully.")
        #knowledge retrieval for learning information
        #-----------------------------------------

        message_lower = message.lower()

        # ----------------------------------
        # Learning retrieval
        # ----------------------------------

        if "what am i studying" in message_lower:
            knowledge = {
                "Goals": self.knowledge_service.get_goals(),
                "Learning": self.knowledge_service.get_learning(),
                }

            return self.reasoning.recommend_learning(knowledge)

        # ----------------------------------
        # Knowledge summary
        # ----------------------------------

        if "what do you know about me" in message_lower:

            knowledge = self.knowledge_service.get_all()
            

            return self.reasoning.summarize_user(knowledge)

        #-----------------------------------------
        #Continue with the chat process
        #-----------------------------------------

        # Save the user's message
        self.memory.add(
            role="user",
            content=message
        )

        logger.info("User message saved to memory.")

        # Load the system prompt
        system_prompt = self.prompt_service.get("system_prompt.txt")

        messages = self.conversation.build(
            system_prompt=system_prompt,
            history=self.memory.recent(20)
        )

        # Generate AI response 
        response = self.provider.generate(messages)

        logger.info("AI response generated.")

        # Save the assistant's response
        self.memory.add(
            role="assistant",
            content=response
        )

        logger.info("Assistant response saved to memory.")

        return response
        
        
