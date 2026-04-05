from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENVIRONMENT: str = "local"
    PORT: int = 8000
    
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "llm-eval-playground"
    GROQ_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_file_encoding="utf-8", extra="ignore")

settings = Settings()
