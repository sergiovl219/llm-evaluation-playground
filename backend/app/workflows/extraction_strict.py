from app.workflows.base import ExtractionWorkflow
from app.schemas.domain import SupportTicket
from app.services.llm_service import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class StrictExtraction(ExtractionWorkflow):
    def __init__(self, model_id: str = "llama-3.1-8b-instant"):
        super().__init__(model_id)
        # Enforcing JSON mode in model
        self.llm = get_llm(model_id).bind(response_format={"type": "json_object"})
        
        system_instructions = """You are a highly capable data extraction system.
You MUST extract the following information from the user's support ticket and return it as a VALID JSON object.
        
Required fields (all must be present):
- ticket_id: string or null
- customer_name: string or null
- issue_category: string (must be one of: billing, technical, login, bug, feature_request, other)
- priority: string (must be one of: low, medium, high, critical)
- summary: string (exactly 1 sentence)
- mentioned_products: array of strings
        
Do not include any extra fields or markdown syntax. Output JSON ONLY.
"""
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_instructions),
            ("user", "{text}")
        ])
        
        self.chain = self.prompt | self.llm | JsonOutputParser()
        
    async def extract(self, text: str) -> SupportTicket:
        try:
            data = await self.chain.ainvoke({"text": text})
            return SupportTicket(**data)
        except Exception as e:
            return SupportTicket(
                issue_category="unknown",
                priority="low",
                summary=f"Strict extraction error: {str(e)}"
            )
