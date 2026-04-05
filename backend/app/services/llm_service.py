from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

def get_llm(model_id: str = "llama-3.1-8b-instant", temperature: float = 0.0):
    """
    Factory para adquirir el LLM dinámicamente dependiendo del proveedor inferido.
    """
    if model_id.startswith("gemini"):
        return ChatGoogleGenerativeAI(
            model=model_id,
            temperature=temperature,
            google_api_key=settings.GOOGLE_API_KEY
        )
    else:
        return ChatGroq(
            model=model_id,
            temperature=temperature,
            api_key=settings.GROQ_API_KEY
        )
