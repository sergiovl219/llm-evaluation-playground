import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health
from app.config import settings

def create_app() -> FastAPI:
    if settings.LANGCHAIN_API_KEY:
        os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
        
    app = FastAPI(
        title="LLM Evaluation Playground",
        description="API for testing and evaluating LLM workflows",
        version="0.1.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allow all for MVP frontend dev
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.routes import playground, evaluations
    # Routers
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(playground.router, prefix="/api", tags=["playground"])
    app.include_router(evaluations.router, prefix="/api", tags=["evaluations"])
    
    return app

app = create_app()
