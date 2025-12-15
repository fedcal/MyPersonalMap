"""
Configuration Manager

Manages application configuration for standalone executables.
Handles user data directory creation and .env file management.
"""

from pathlib import Path
import platform
import shutil
from typing import Optional
import logging


logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages configuration for standalone executable

    Creates OS-specific user data directories and manages .env configuration file.

    User Data Directories:
        - Windows: %LOCALAPPDATA%/MyPersonalMap
        - macOS: ~/Library/Application Support/MyPersonalMap
        - Linux: ~/.local/share/MyPersonalMap

    Example:
        config_mgr = ConfigManager()
        env_path = config_mgr.init_config()
        # Use env_path with python-dotenv
    """

    def __init__(self, app_name: str = "MyPersonalMap"):
        """
        Initialize ConfigManager

        Args:
            app_name: Application name for directory naming
        """
        self.app_name = app_name
        self.user_data_dir = self.get_user_data_dir()
        self.config_file = self.user_data_dir / ".env"
        self.db_file = self.user_data_dir / "mypersonalmap.db"  # SQLite fallback

    @staticmethod
    def get_user_data_dir() -> Path:
        """
        Get OS-specific user data directory

        Returns:
            Path to user data directory

        Examples:
            Windows: C:/Users/user/AppData/Local/MyPersonalMap
            macOS: /Users/user/Library/Application Support/MyPersonalMap
            Linux: /home/user/.local/share/MyPersonalMap
        """
        system = platform.system()

        if system == "Windows":
            base = Path.home() / "AppData" / "Local"
        elif system == "Darwin":  # macOS
            base = Path.home() / "Library" / "Application Support"
        else:  # Linux and others
            base = Path.home() / ".local" / "share"

        return base / "MyPersonalMap"

    def init_config(self) -> Path:
        """
        Initialize configuration

        Creates user data directory and .env file if they don't exist.

        Returns:
            Path to .env file
        """
        # Create user data directory
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"User data directory: {self.user_data_dir}")

        # Create .env if it doesn't exist
        if not self.config_file.exists():
            self._create_default_env()
            logger.info(f"Created default .env at {self.config_file}")
        else:
            logger.info(f"Using existing .env at {self.config_file}")

        return self.config_file

    def _create_default_env(self):
        """
        Create default .env file with template values

        User must edit this file with their actual database credentials.
        """
        default_env = """# My Personal Map - Configuration
# Edit this file with your database credentials

# ==================== DATABASE ====================
DATABASE_USER=mypersonalmap_user
DATABASE_PASSWORD=CHANGE_ME
DATABASE_URL=localhost
DATABASE_NAME=mypersonalmap
DATABASE_PORT=3306

# ==================== SECURITY ====================
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(64))"
SECRET_KEY=CHANGE_ME_GENERATE_NEW_KEY

# ==================== APPLICATION ====================
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# ==================== API ====================
CORS_ORIGINS=http://localhost:8000

# ==================== GEOCODING ====================
GEOCODING_PROVIDER=nominatim
GEOCODING_USER_AGENT=MyPersonalMap/1.0
"""
        self.config_file.write_text(default_env)

    def get_env_path(self) -> Path:
        """
        Get path to .env configuration file

        Returns:
            Path to .env file
        """
        return self.config_file

    def get_logs_dir(self) -> Path:
        """
        Get directory for application logs

        Returns:
            Path to logs directory
        """
        logs_dir = self.user_data_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        return logs_dir

    def get_cache_dir(self) -> Path:
        """
        Get directory for cache files

        Returns:
            Path to cache directory
        """
        cache_dir = self.user_data_dir / "cache"
        cache_dir.mkdir(exist_ok=True)
        return cache_dir

    def get_exports_dir(self) -> Path:
        """
        Get directory for exported files (GPX, KML, etc.)

        Returns:
            Path to exports directory
        """
        exports_dir = self.user_data_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        return exports_dir

    def backup_config(self, backup_name: Optional[str] = None) -> Path:
        """
        Backup current .env file

        Args:
            backup_name: Optional backup filename (default: .env.backup)

        Returns:
            Path to backup file
        """
        if not self.config_file.exists():
            raise FileNotFoundError("No config file to backup")

        backup_name = backup_name or ".env.backup"
        backup_path = self.user_data_dir / backup_name
        shutil.copy2(self.config_file, backup_path)
        logger.info(f"Config backed up to {backup_path}")

        return backup_path

    def reset_config(self):
        """
        Reset configuration to defaults

        WARNING: This will overwrite the current .env file!
        """
        # Backup current config first
        if self.config_file.exists():
            self.backup_config(".env.backup.old")

        # Create new default config
        self._create_default_env()
        logger.warning("Configuration reset to defaults")
