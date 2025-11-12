from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application Settings loading from the environment variables"""

    # MongoDB Configuration
    MONGODB_URL: str
    DATABASE_NAME: str

    # Application Configuration
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = True

    # CORS Settings
    ALLOWED_ORIGINS: List[str]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

# Singleton Class -> Instance
settings = Settings()
