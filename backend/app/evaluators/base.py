from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseEvaluator(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the evaluator"""
        pass
        
    @abstractmethod
    def evaluate(self, prediction: Any, reference: Any) -> Dict[str, Any]:
        """
        Evaluate a prediction against a reference.
        Returns a dictionary containing at least a 'score' (0.0 to 1.0) and optionally 'details'.
        """
        pass
