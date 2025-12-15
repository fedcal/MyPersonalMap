"""
Application Settings

Configurazioni caricate da pymypersonalmap/.env tramite python-dotenv
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Determina il path del .env in base all'ambiente (development vs standalone)
if getattr(sys, 'frozen', False):
    # Eseguibile PyInstaller: usa config manager per user data directory
    # Questo import viene fatto solo se frozen per evitare import circolari
    try:
        from pymypersonalmap.gui.config_manager import ConfigManager
        config_mgr = ConfigManager()
        env_path = config_mgr.init_config()
    except ImportError:
        # Fallback se config_manager non esiste ancora
        env_path = Path.home() / '.mypersonalmap' / '.env'
else:
    # Development: usa SEMPRE .env nella directory pymypersonalmap
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        raise FileNotFoundError(
            f"File .env non trovato in {env_path}\n"
            "Crea il file pymypersonalmap/.env con le tue configurazioni."
        )

load_dotenv(dotenv_path=env_path)

# ==================== DATABASE ====================
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_URL = os.getenv("DATABASE_URL")  # Host
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "3306"))

# ==================== SERVER ====================
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
WORKERS_COUNT = int(os.getenv("WORKERS_COUNT", "4"))

# ==================== SECURITY ====================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# ==================== GEOCODING ====================
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

# ==================== APPLICATION ====================
APP_NAME = os.getenv("APP_NAME", "MyPersonalMap")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

# ==================== API ====================
API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080")

# ==================== GEOCODING EXTRA ====================
GEOCODING_PROVIDER = os.getenv("GEOCODING_PROVIDER", "nominatim")
GEOCODING_USER_AGENT = os.getenv("GEOCODING_USER_AGENT", "MyPersonalMap/1.0")
GEOCODING_RATE_LIMIT_SECONDS = int(os.getenv("GEOCODING_RATE_LIMIT_SECONDS", "1"))

# ==================== FILE UPLOAD ====================
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
ALLOWED_IMPORT_FORMATS = os.getenv("ALLOWED_IMPORT_FORMATS", "gpx,kml,geojson,csv")

# ==================== FEATURE FLAGS ====================
ENABLE_WEB_SCRAPING = os.getenv("ENABLE_WEB_SCRAPING", "false").lower() == "true"
ENABLE_STATISTICS = os.getenv("ENABLE_STATISTICS", "true").lower() == "true"
ENABLE_SHARING = os.getenv("ENABLE_SHARING", "true").lower() == "true"

# ==================== COMPUTED VALUES ====================
# Costruisce DATABASE_URL completo dalle componenti
database_url = (
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Alias per compatibilità
host = SERVER_HOST
port = SERVER_PORT
workers = WORKERS_COUNT
