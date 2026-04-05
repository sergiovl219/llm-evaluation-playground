from typing import Dict, Any
from app.evaluators.base import BaseEvaluator
from app.schemas.domain import SupportTicket

class FormatValidityEvaluator(BaseEvaluator):
    @property
    def name(self) -> str:
        return "format_validity"
        
    def evaluate(self, prediction: Any, reference: Any) -> Dict[str, Any]:
        is_valid = isinstance(prediction, SupportTicket)
        
        if is_valid and getattr(prediction, "issue_category", None) == "unknown" and "error" in str(getattr(prediction, "summary", "")).lower():
            is_valid = False
            
        return {
            "score": 1.0 if is_valid else 0.0,
            "details": {"is_valid": is_valid}
        }
