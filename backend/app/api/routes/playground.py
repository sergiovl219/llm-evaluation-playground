from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.workflows.extraction_baseline import BaselineExtraction
from app.workflows.extraction_strict import StrictExtraction
from app.workflows.extraction_structured import StructuredExtraction

router = APIRouter()

class ExecutionRequest(BaseModel):
    workflow_strategy: str
    model_id: str = "llama-3.1-8b-instant"
    input_text: str

def get_workflow(strategy: str, model_id: str):
    if strategy == "baseline":
        return BaselineExtraction(model_id)
    elif strategy == "strict":
        return StrictExtraction(model_id)
    elif strategy == "structured":
        return StructuredExtraction(model_id)
    return None

@router.post("/execute")
async def execute_workflow(request: ExecutionRequest):
    workflow = get_workflow(request.workflow_strategy, request.model_id)
    if not workflow:
        raise HTTPException(status_code=400, detail="Invalid workflow strategy")
        
    try:
        result = await workflow.extract(request.input_text)
        return {"result": result.model_dump(), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
