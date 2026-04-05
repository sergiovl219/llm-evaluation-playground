from typing import Dict, Any
from app.evaluators.base import BaseEvaluator
from app.schemas.domain import SupportTicket

class FieldCoverageEvaluator(BaseEvaluator):
    @property
    def name(self) -> str:
        return "field_coverage"
        
    def evaluate(self, prediction: Any, reference: Any) -> Dict[str, Any]:
        if not isinstance(prediction, SupportTicket):
            return {"score": 0.0, "details": {"error": "Invalid format"}}
            
        pred_dict = prediction.model_dump()
        expected_keys = ["ticket_id", "customer_name", "issue_category", "priority", "summary", "mentioned_products"]
        
        covered = 0
        details = {}
        for key in expected_keys:
            val = pred_dict.get(key)
            if val is not None:
                covered += 1
                details[key] = True
            else:
                details[key] = False
                
        return {
            "score": covered / len(expected_keys),
            "details": details
        }
