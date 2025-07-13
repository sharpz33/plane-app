from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AMADEUS_API_KEY: str
    AMADEUS_API_SECRET: str

settings = Settings()