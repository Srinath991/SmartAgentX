from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    MODEL_NAME: str = "gemini-pro"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    LANGSMITH_API_KEY:str=os.getenv("LANGSMITH_API_KEY", "")
    OPENWEATHER_API_KEY:str=os.getenv("OPENWEATHER_API_KEY", "")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 