"""
Application Settings

Centralized configuration management using pydantic-settings.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application configuration settings"""

    # Application
    APP_NAME: str = "MyPersonalMap"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Database
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/mypersonalmap"
    DB_ECHO: bool = False

    # Security
    SECRET_KEY: str = "change-this-secret-key-min-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

    # Geocoding
    GEOCODING_PROVIDER: str = "nominatim"
    GEOCODING_USER_AGENT: str = "MyPersonalMap/1.0"
    GEOCODING_RATE_LIMIT_SECONDS: int = 1
    GOOGLE_MAPS_API_KEY: str = ""

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_IMPORT_FORMATS: str = "gpx,kml,geojson,csv"

    # Feature Flags
    ENABLE_WEB_SCRAPING: bool = False
    ENABLE_STATISTICS: bool = True
    ENABLE_SHARING: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def allowed_formats_list(self) -> List[str]:
        """Parse allowed formats string to list"""
        return [fmt.strip() for fmt in self.ALLOWED_IMPORT_FORMATS.split(",")]


# Global settings instance
settings = Settings()
