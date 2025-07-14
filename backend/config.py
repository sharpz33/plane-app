# backend/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Amadeus keys
    AMADEUS_API_KEY: str
    AMADEUS_API_SECRET: str
    
    # Mailgun API configuration
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN: str

settings = Settings()