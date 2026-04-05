from abc import ABC, abstractmethod
from app.schemas.domain import SupportTicket

class ExtractionWorkflow(ABC):
    def __init__(self, model_id: str):
        self.model_id = model_id
        
    @abstractmethod
    async def extract(self, text: str) -> SupportTicket:
        """Execute the workflow on the given text and return structured output."""
        pass
