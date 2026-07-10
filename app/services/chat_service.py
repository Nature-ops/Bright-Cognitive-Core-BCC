

from urllib import response

from app.services.ai.ollama_provider import OllamaProvider
from app.services.prompt_service import PromptService
from app.services.memory_service import MemoryService
from app.utils.logger import logger
from app.services.conversation_service import ConversationService
from app.services.memory_classifier import MemoryClassifier
from app.services.knowledge_service import KnowledgeService


class ChatService:
    def __init__(self):
        self.provider = OllamaProvider()
        self.knowledge_service = KnowledgeService()
        self.prompt_service = PromptService()
        self.memory = MemoryService()
        self.conversation = ConversationService()
        self.classifier = MemoryClassifier()

    def chat(self, message: str) -> str:
        

        logger.info(f"Received message: {message}")
        
        classification = self.classifier.classify(message)
        
        logger.info(
            f"Message classified as: {classification}"
        )
        self.knowledge_service.store_classification(
            classification,
              message
        )
        logger.info(
            "Knowledge stored successfully."
        )
#-----------------------------------------
#knowledge retrieval for learning information
#-----------------------------------------



        message_lower = message.lower()

        if "what am i studying" in message_lower:

            learning = self.knowledge_service.get_learning()

            if learning:

                knowledge_response = "you are currently studying:\n\n"

                for item in learning:
                    knowledge_response += f"- {item['content']}\n"
                    
                return knowledge_response
                 
            return "I don't have any learning information stored  yet."


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
        
        
