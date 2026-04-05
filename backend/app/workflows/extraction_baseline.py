import json
from app.workflows.base import ExtractionWorkflow
from app.schemas.domain import SupportTicket
from app.services.llm_service import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class BaselineExtraction(ExtractionWorkflow):
    def __init__(self, model_id: str = "llama-3.1-8b-instant"):
        super().__init__(model_id)
        self.llm = get_llm(model_id)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Extract information from the support ticket into JSON format. Include fields for ticket_id, customer_name, issue_category, priority, summary, mentioned_products."),
            ("user", "{text}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
        
    async def extract(self, text: str) -> SupportTicket:
        raw_output = await self.chain.ainvoke({"text": text})
        
        # Try a naive parsing
        try:
            clean_str = raw_output.strip()
            if clean_str.startswith("```json"):
                clean_str = clean_str[7:-3]
            elif clean_str.startswith("```"):
                clean_str = clean_str[3:-3]
            data = json.loads(clean_str.strip())
            return SupportTicket(**data)
        except Exception:
            # Baseline doesn't have strict recovery
            return SupportTicket(
                issue_category="unknown",
                priority="low",
                summary=f"Extraction Error. Raw Output: {raw_output[:50]}..."
            )
