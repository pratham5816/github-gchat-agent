import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # LLM Settings
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    
    # GitHub Settings
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_API_KEY") or os.getenv("GITHUB_TOKEN")
    GITHUB_USER: str = os.getenv("USER", "pratham5816")
    
    # Google Chat Settings
    GOOGLE_CHAT_API: Optional[str] = os.getenv("GOOGLE_CHAT_API")
    GCHAT_WEBHOOK_URL: Optional[str] = os.getenv("GCHAT_WEBHOOK_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
