from fastapi import APIRouter, HTTPException
import json
import os
from pydantic import BaseModel
from typing import List, Dict, Any
from app.api.routes.playground import get_workflow
from app.evaluators.exact_match import ExactMatchEvaluator
from app.evaluators.format_validity import FormatValidityEvaluator
from app.evaluators.field_coverage import FieldCoverageEvaluator

router = APIRouter()

evaluators = [
    ExactMatchEvaluator(),
    FormatValidityEvaluator(),
    FieldCoverageEvaluator()
]

class EvaluationRequest(BaseModel):
    workflow_strategy: str
    model_id: str = "llama-3.1-8b-instant"

@router.post("/evaluate")
async def run_evaluation(request: EvaluationRequest):
    workflow = get_workflow(request.workflow_strategy, request.model_id)
    if not workflow:
        raise HTTPException(status_code=400, detail="Invalid workflow strategy")
        
    # Load dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "../../../../data/datasets/extraction_dataset.json")
    try:
        with open(dataset_path, "r") as f:
            dataset = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load dataset: {e}")
        
    results = []
    
    for item in dataset:
        input_text = item["input_text"]
        expected = item["expected_output"]
        
        try:
            prediction = await workflow.extract(input_text)
            
            item_evals = {}
            for evaluator in evaluators:
                item_evals[evaluator.name] = evaluator.evaluate(prediction, expected)
                
            results.append({
                "input": input_text,
                "expected": expected,
                "prediction": prediction.model_dump() if prediction else None,
                "evaluations": item_evals
            })
        except Exception as e:
            results.append({
                "input": input_text,
                "error": str(e)
            })
            
    # Calculate aggregates
    summary = {}
    valid_results = [r for r in results if "error" not in r]
    
    for evaluator in evaluators:
        if valid_results:
            avg_score = sum(r["evaluations"][evaluator.name]["score"] for r in valid_results) / len(valid_results)
            summary[evaluator.name] = avg_score
        else:
            summary[evaluator.name] = 0.0
            
    return {
        "summary": summary,
        "results": results
    }
