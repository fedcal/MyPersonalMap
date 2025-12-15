"""
My Personal Map - Desktop Application

Main entry point for the GUI application.
Manages window, backend, database setup, and layout.
"""

import customtkinter as ctk
import sys
import logging
from pathlib import Path

from pymypersonalmap.gui.theme import init_theme
from pymypersonalmap.gui.layouts.main_layout import MainLayout
from pymypersonalmap.gui.backend_manager import BackendManager
from pymypersonalmap.gui.setup_wizard import DatabaseSetupWizard
from pymypersonalmap.gui.config_manager import ConfigManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MyPersonalMapApp(ctk.CTk):
    """
    Main application window

    Manages:
        - Application window and theme
        - Backend server (FastAPI in thread)
        - Database setup wizard
        - Main layout and navigation

    Example:
        app = MyPersonalMapApp()
        app.mainloop()
    """

    def __init__(self):
        """Initialize application"""
        super().__init__()

        # Window configuration
        self.title("My Personal Map")
        self.geometry("1400x900")
        self.minsize(1024, 768)

        # Center window on screen
        self.center_window()

        # Initialize theme
        init_theme(mode="dark")

        # Config manager
        self.config_mgr = ConfigManager()

        # Backend manager (will be started after DB setup)
        self.backend = BackendManager(host="127.0.0.1", port=8000)

        # Check database setup
        if not self.check_database_configured():
            logger.info("Database not configured, showing setup wizard")
            self.show_setup_wizard()
        else:
            logger.info("Database already configured")
            self.start_application()

    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def check_database_configured(self) -> bool:
        """
        Check if database is configured and accessible

        Returns:
            True if database is ready, False otherwise
        """
        try:
            # Try to import and check database connection
            from pymypersonalmap.database.session import engine
            from sqlalchemy import inspect, text

            # Test connection
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            # Check if tables exist
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            if len(tables) > 0:
                logger.info(f"Database configured with {len(tables)} tables")
                return True
            else:
                logger.warning("Database connected but no tables found")
                return False

        except Exception as e:
            logger.warning(f"Database not accessible: {e}")
            return False

    def show_setup_wizard(self):
        """Show database setup wizard"""
        wizard = DatabaseSetupWizard(self, on_complete=self.on_wizard_complete)

        # Wait for wizard to complete
        self.wait_window(wizard)

        # Check if wizard was completed successfully
        if not wizard.db_configured:
            logger.error("Database setup was not completed")
            self.show_error_and_exit(
                "Database setup is required to run the application.\n"
                "Please restart and complete the setup wizard."
            )

    def on_wizard_complete(self):
        """Callback when setup wizard completes"""
        logger.info("Setup wizard completed successfully")
        self.start_application()

    def start_application(self):
        """Start the application (backend + GUI)"""
        try:
            # Start backend
            logger.info("Starting backend server...")
            self.backend.start()
            logger.info("Backend started successfully")

            # Initialize database tables if needed
            self.initialize_database()

            # Load main layout
            self.main_layout = MainLayout(self)
            self.main_layout.pack(fill="both", expand=True)

            logger.info("Application started successfully")

        except TimeoutError as e:
            logger.error(f"Backend failed to start: {e}")
            self.show_error_and_exit(
                f"Failed to start backend server:\n{str(e)}\n\n"
                "Please check if port 8000 is available."
            )
        except Exception as e:
            logger.error(f"Application startup failed: {e}", exc_info=True)
            self.show_error_and_exit(
                f"Application failed to start:\n{str(e)}\n\n"
                "Check logs for details."
            )

    def initialize_database(self):
        """Initialize database tables and system data"""
        try:
            from pymypersonalmap.database.session import engine, init_db, SessionLocal
            from pymypersonalmap.services import label_service
            from sqlalchemy import inspect

            # Check if tables exist
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()

            if not existing_tables:
                logger.info("Creating database tables...")
                init_db()
                logger.info("Database tables created")

                # Initialize system labels
                logger.info("Initializing system labels...")
                db = SessionLocal()
                try:
                    label_service.initialize_system_labels(db)
                    logger.info("System labels initialized")
                except Exception as e:
                    logger.warning(f"Failed to initialize system labels: {e}")
                finally:
                    db.close()
            else:
                logger.info(f"Database already initialized ({len(existing_tables)} tables)")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def show_error_and_exit(self, message: str):
        """
        Show error dialog and exit application

        Args:
            message: Error message to display
        """
        # Create error dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("500x300")

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 150
        dialog.geometry(f"+{x}+{y}")

        # Error icon
        icon_label = ctk.CTkLabel(
            dialog,
            text="❌",
            font=("Arial", 48),
        )
        icon_label.pack(pady=(30, 10))

        # Error message
        msg_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=("Arial", 14),
            wraplength=450,
        )
        msg_label.pack(pady=20, padx=20)

        # Exit button
        exit_btn = ctk.CTkButton(
            dialog,
            text="Exit",
            command=lambda: sys.exit(1),
            width=100,
            height=40,
        )
        exit_btn.pack(pady=20)

        # Wait for dialog
        self.wait_window(dialog)
        sys.exit(1)

    def on_closing(self):
        """Handle window close event"""
        logger.info("Application closing...")

        # Stop backend
        if hasattr(self, 'backend') and self.backend.is_running:
            logger.info("Stopping backend...")
            self.backend.stop()

        # Destroy window
        self.destroy()


def main():
    """
    Main entry point

    Usage:
        python pymypersonalmap/gui/app.py

    Or with package installed:
        mypersonalmap
    """
    try:
        app = MyPersonalMapApp()

        # Handle window close
        app.protocol("WM_DELETE_WINDOW", app.on_closing)

        # Start main loop
        app.mainloop()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
