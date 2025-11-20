from typing import List
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from the environment.
    
    All settings can be overridden via environment variables or .env file.
    Critical settings are validated to ensure production readiness.
    """

    APP_NAME: str = "Product-Inventory-API"
    APP_VERSION: str = "1.0.0"
    
    # Environment
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")

    # CORS Settings - More restrictive by default
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        description="List of allowed CORS origins"
    )

    DEBUG: bool = Field(default=False, description="Enable debug mode (disable in production)")

    # Database Settings
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection string"
    )
    DATABASE_NAME: str = Field(
        default="product_inventory",
        description="MongoDB database name"
    )

    # Logger Settings
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    LOG_DIR: str = Field(default="logs", description="Directory for log files")
    LOG_TO_CONSOLE: bool = Field(default=True, description="Enable console logging")
    LOG_TO_FILE: bool = Field(default=True, description="Enable file logging")
    LOG_USE_COLORS: bool = Field(default=True, description="Use colored console output")
    
    # API Settings
    API_V1_PREFIX: str = Field(default="/api/v1", description="API version prefix")
    MAX_PAGE_SIZE: int = Field(default=100, description="Maximum items per page for pagination")
    DEFAULT_PAGE_SIZE: int = Field(default=10, description="Default items per page")

    # Security Settings
    ENABLE_SECURITY_HEADERS: bool = Field(
        default=True,
        description="Enable security headers middleware"
    )
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the accepted values."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}, got {v}")
        return v
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment is one of the accepted values."""
        valid_envs = ["development", "staging", "production"]
        v = v.lower()
        if v not in valid_envs:
            raise ValueError(f"ENVIRONMENT must be one of {valid_envs}, got {v}")
        return v
    
    @field_validator("MONGODB_URL")
    @classmethod
    def validate_mongodb_url(cls, v: str) -> str:
        """Validate MongoDB URL format."""
        if not v.startswith(("mongodb://", "mongodb+srv://")):
            raise ValueError(
                "MONGODB_URL must start with 'mongodb://' or 'mongodb+srv://'"
            )
        return v
    
    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def validate_origins(cls, v: List[str]) -> List[str]:
        """Ensure ALLOWED_ORIGINS is not set to wildcard in production."""
        if "*" in v:
            import os
            env = os.getenv("ENVIRONMENT", "development").lower()
            if env == "production":
                raise ValueError(
                    "Wildcard '*' not allowed in ALLOWED_ORIGINS for production environment"
                )
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT.lower() == "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
        env_file_encoding="utf-8"
    )


settings = Settings()
