from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database - Use PostgreSQL for production, SQLite for development
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./totus_tuus.db")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here-make-it-long-and-secure")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # API
    api_v1_str: str = os.getenv("API_V1_STR", "/api/v1")
    project_name: str = os.getenv("PROJECT_NAME", "Totus Tuus - App de Consagración Total")
    
    # CORS
    def get_cors_origins(self) -> List[str]:
        cors_env = os.getenv("BACKEND_CORS_ORIGINS", "")
        if cors_env:
            return [origin.strip() for origin in cors_env.split(",")]
        return [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://localhost:8080"
        ]
    
    @property
    def backend_cors_origins(self) -> List[str]:
        return self.get_cors_origins()
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Debug mode - disables day progression timer for testing
    debug_mode: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    class Config:
        case_sensitive = True

settings = Settings() 