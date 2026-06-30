from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
import logging

logger = logging.getLogger(__name__)



class BaseAgent:

    """
    Base class all agents inherit from.
    Uses Ollama (local Llama 3.2) — no API key, no rate limits.
    """

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = ChatOllama(
            model="mistral",        # changed from llama3.2 to mistral
            temperature=0.2,
            base_url="http://localhost:11434"
        )
        logger.info(f"Agent initialized: {self.name} (Ollama/Mistral)")

    def run(self, user_message: str) -> str:
        """Send a message to local Llama and get a response."""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_message)
        ]
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Ollama error in {self.name}: {e}")
            raise

    def __repr__(self):
        return f"<Agent: {self.name} | Ollama>"