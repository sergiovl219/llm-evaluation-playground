from app.workflows.base import ExtractionWorkflow
from app.schemas.domain import SupportTicket
from app.services.llm_service import get_llm
from langchain_core.prompts import ChatPromptTemplate

class StructuredExtraction(ExtractionWorkflow):
    def __init__(self, model_id: str = "llama-3.1-8b-instant"):
        super().__init__(model_id)
        self.llm = get_llm(model_id)
        # Using native tool calling / JSON mode under the hood
        self.structured_llm = self.llm.with_structured_output(SupportTicket)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert technical support assistant. Extract the requested fields from the user's support ticket."),
            ("user", "{text}")
        ])
        
        self.chain = self.prompt | self.structured_llm
        
    async def extract(self, text: str) -> SupportTicket:
        result = await self.chain.ainvoke({"text": text})
        return result
