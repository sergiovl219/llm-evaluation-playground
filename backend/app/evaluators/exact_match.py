from typing import Dict, Any
from app.evaluators.base import BaseEvaluator
from app.schemas.domain import SupportTicket

class ExactMatchEvaluator(BaseEvaluator):
    @property
    def name(self) -> str:
        return "exact_match_categorical"
        
    def evaluate(self, prediction: Any, reference: dict) -> Dict[str, Any]:
        if not isinstance(prediction, SupportTicket):
            return {"score": 0.0, "details": {"error": "Prediction is not a SupportTicket"}}
            
        score = 0.0
        details = {}
        
        pred_dict = prediction.model_dump()
        
        if pred_dict.get("issue_category") == reference.get("issue_category"):
            score += 0.5
            details["issue_category"] = True
        else:
            details["issue_category"] = False
            
        if pred_dict.get("priority") == reference.get("priority"):
            score += 0.5
            details["priority"] = True
        else:
            details["priority"] = False
            
        return {
            "score": score,
            "details": details
        }
