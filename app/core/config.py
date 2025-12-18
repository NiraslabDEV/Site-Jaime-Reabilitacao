from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # M-Pesa API
    MPESA_API_KEY: str = ""
    MPESA_API_URL: str = "https://api.mpesa.com"  # Ajustar conforme necessário
    MPESA_ENVIRONMENT: str = "sandbox"  # sandbox ou production
    MPESA_CALLBACK_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


