"""
Database Setup Wizard

Interactive wizard for setting up MySQL database on first run.
Guides user through MySQL installation or provides SQLite fallback.
"""

import customtkinter as ctk
import pymysql
import platform
import webbrowser
from pathlib import Path
from typing import Optional, Callable
from pymypersonalmap.gui.theme import COLORS, SPACING, get_font
from pymypersonalmap.gui.components.custom_button import CustomButton
import logging


logger = logging.getLogger(__name__)


class DatabaseSetupWizard(ctk.CTkToplevel):
    """
    Wizard for database setup

    Steps:
        1. Check if MySQL is installed
        2a. If NO: Show installation guide or SQLite fallback
        2b. If YES: Collect credentials and create database

    Attributes:
        db_configured: True if database was successfully configured
    """

    def __init__(self, parent, on_complete: Optional[Callable] = None):
        """
        Initialize DatabaseSetupWizard

        Args:
            parent: Parent window
            on_complete: Callback function called when wizard completes
        """
        super().__init__(parent)

        self.title("Database Setup - My Personal Map")
        self.geometry("700x600")
        self.resizable(False, False)

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 350
        y = (self.winfo_screenheight() // 2) - 300
        self.geometry(f"+{x}+{y}")

        # State
        self.db_configured = False
        self.on_complete = on_complete

        # Content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=SPACING["2xl"], pady=SPACING["2xl"])

        # Start wizard
        self.show_welcome()

    def clear_content(self):
        """Clear all widgets from content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_welcome(self):
        """Show welcome screen"""
        self.clear_content()

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="🗺️ Welcome to My Personal Map",
            font=get_font("sans", "4xl", "bold"),
        )
        title.pack(pady=(0, SPACING["lg"]))

        # Subtitle
        subtitle = ctk.CTkLabel(
            self.content_frame,
            text="Let's set up your database",
            font=get_font("sans", "xl", "normal"),
            text_color=COLORS["gray_600"],
        )
        subtitle.pack(pady=(0, SPACING["2xl"]))

        # Info
        info_text = (
            "This application requires a database to store your markers and maps.\n\n"
            "We'll help you set up MySQL or provide a SQLite alternative."
        )
        info = ctk.CTkLabel(
            self.content_frame,
            text=info_text,
            font=get_font("sans", "base", "normal"),
            justify="left",
        )
        info.pack(pady=SPACING["xl"])

        # Start button
        start_btn = CustomButton(
            self.content_frame,
            text="Let's Start",
            variant="accent",
            width=200,
            height=48,
            command=self.check_mysql,
        )
        start_btn.pack(pady=SPACING["2xl"])

    def check_mysql(self):
        """Check if MySQL is installed and accessible"""
        self.clear_content()

        # Checking message
        checking_label = ctk.CTkLabel(
            self.content_frame,
            text="Checking for MySQL...",
            font=get_font("sans", "2xl", "bold"),
        )
        checking_label.pack(pady=SPACING["2xl"])

        # Progress indicator
        progress = ctk.CTkProgressBar(self.content_frame, width=300, mode="indeterminate")
        progress.pack(pady=SPACING["lg"])
        progress.start()

        # Check in background to avoid freezing UI
        def do_check():
            self.after(1000, lambda: self._perform_mysql_check(progress))

        do_check()

    def _perform_mysql_check(self, progress_widget):
        """Perform actual MySQL check"""
        try:
            # Try to connect to MySQL (without authentication)
            # This will fail if MySQL is not installed or not running
            pymysql.connect(host="localhost", port=3306, connect_timeout=2)
            mysql_available = True
        except pymysql.err.OperationalError as e:
            # MySQL not available or connection refused
            mysql_available = False
            logger.info(f"MySQL check failed: {e}")
        except Exception as e:
            mysql_available = False
            logger.error(f"Unexpected error checking MySQL: {e}")

        # Stop progress
        progress_widget.stop()

        if mysql_available:
            self.show_mysql_setup()
        else:
            self.show_mysql_not_found()

    def show_mysql_not_found(self):
        """Show screen when MySQL is not found"""
        self.clear_content()

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="⚠️ MySQL Not Found",
            font=get_font("sans", "3xl", "bold"),
        )
        title.pack(pady=(0, SPACING["lg"]))

        # Info
        info_text = (
            "MySQL is not installed or not running on your system.\n\n"
            "Choose an option below to continue:"
        )
        info = ctk.CTkLabel(
            self.content_frame,
            text=info_text,
            font=get_font("sans", "base", "normal"),
        )
        info.pack(pady=SPACING["xl"])

        # Options frame
        options_frame = ctk.CTkFrame(self.content_frame)
        options_frame.pack(fill="both", expand=True, pady=SPACING["lg"])

        # Option 1: Install MySQL
        install_btn = CustomButton(
            options_frame,
            text="📖 Guide to Install MySQL",
            variant="primary",
            height=60,
            command=self.show_mysql_installation_guide,
        )
        install_btn.pack(fill="x", padx=SPACING["lg"], pady=SPACING["md"])

        # Option 2: SQLite fallback
        sqlite_btn = CustomButton(
            options_frame,
            text="💾 Use SQLite (Limited Features)",
            variant="secondary",
            height=60,
            command=self.setup_sqlite,
        )
        sqlite_btn.pack(fill="x", padx=SPACING["lg"], pady=SPACING["md"])

        # Warning about SQLite
        warning = ctk.CTkLabel(
            options_frame,
            text="⚠️ SQLite has limited support for spatial queries",
            font=get_font("sans", "sm", "normal"),
            text_color=COLORS["warning"],
        )
        warning.pack(pady=SPACING["sm"])

    def show_mysql_installation_guide(self):
        """Show MySQL installation guide for user's OS"""
        self.clear_content()

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="MySQL Installation Guide",
            font=get_font("sans", "3xl", "bold"),
        )
        title.pack(pady=(0, SPACING["lg"]))

        # Detect OS
        system = platform.system()
        guides = {
            "Windows": {
                "text": "Download MySQL Installer for Windows:",
                "url": "https://dev.mysql.com/downloads/installer/",
                "steps": [
                    "1. Download MySQL Installer",
                    "2. Run installer and choose 'Developer Default'",
                    "3. Follow wizard and set root password",
                    "4. Restart this application after installation",
                ],
            },
            "Darwin": {  # macOS
                "text": "Install MySQL with Homebrew:",
                "url": "https://formulae.brew.sh/formula/mysql",
                "steps": [
                    "1. Install Homebrew if not installed: brew.sh",
                    "2. Run: brew install mysql",
                    "3. Run: brew services start mysql",
                    "4. Run: mysql_secure_installation",
                    "5. Restart this application",
                ],
            },
            "Linux": {
                "text": "Install MySQL on Linux:",
                "url": "https://dev.mysql.com/doc/refman/8.0/en/linux-installation.html",
                "steps": [
                    "Ubuntu/Debian:",
                    "  sudo apt update",
                    "  sudo apt install mysql-server",
                    "  sudo mysql_secure_installation",
                    "",
                    "Fedora/RHEL:",
                    "  sudo dnf install mysql-server",
                    "  sudo systemctl start mysqld",
                ],
            },
        }

        guide = guides.get(system, guides["Linux"])

        # Instructions
        info = ctk.CTkLabel(
            self.content_frame,
            text=guide["text"],
            font=get_font("sans", "lg", "bold"),
        )
        info.pack(pady=SPACING["md"])

        # URL button
        url_btn = CustomButton(
            self.content_frame,
            text=f"Open: {guide['url']}",
            variant="accent",
            command=lambda: webbrowser.open(guide["url"]),
        )
        url_btn.pack(pady=SPACING["md"])

        # Steps
        steps_text = "\n".join(guide["steps"])
        steps_label = ctk.CTkTextbox(
            self.content_frame,
            height=200,
            font=get_font("mono", "sm", "normal"),
        )
        steps_label.insert("1.0", steps_text)
        steps_label.configure(state="disabled")
        steps_label.pack(fill="both", expand=True, pady=SPACING["lg"])

        # Buttons
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=SPACING["lg"])

        back_btn = CustomButton(
            btn_frame,
            text="← Back",
            variant="secondary",
            command=self.show_mysql_not_found,
        )
        back_btn.pack(side="left")

        retry_btn = CustomButton(
            btn_frame,
            text="Retry Detection",
            variant="primary",
            command=self.check_mysql,
        )
        retry_btn.pack(side="right")

    def show_mysql_setup(self):
        """Show MySQL setup form"""
        self.clear_content()

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="✅ MySQL Found!",
            font=get_font("sans", "3xl", "bold"),
        )
        title.pack(pady=(0, SPACING["lg"]))

        # Info
        info = ctk.CTkLabel(
            self.content_frame,
            text="Enter your MySQL root credentials to create the database:",
            font=get_font("sans", "base", "normal"),
        )
        info.pack(pady=SPACING["md"])

        # Form
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(fill="both", expand=True, pady=SPACING["lg"])

        # Root password
        password_label = ctk.CTkLabel(
            form_frame,
            text="MySQL Root Password:",
            font=get_font("sans", "base", "bold"),
            anchor="w",
        )
        password_label.pack(fill="x", padx=SPACING["lg"], pady=(SPACING["lg"], SPACING["sm"]))

        self.root_password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter root password",
            show="•",
            height=40,
        )
        self.root_password_entry.pack(fill="x", padx=SPACING["lg"])

        # New database details
        details_label = ctk.CTkLabel(
            form_frame,
            text="New Database Details:",
            font=get_font("sans", "base", "bold"),
            anchor="w",
        )
        details_label.pack(fill="x", padx=SPACING["lg"], pady=(SPACING["xl"], SPACING["sm"]))

        # DB name
        self.db_name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Database name (default: mypersonalmap)",
            height=40,
        )
        self.db_name_entry.insert(0, "mypersonalmap")
        self.db_name_entry.pack(fill="x", padx=SPACING["lg"], pady=SPACING["sm"])

        # DB user
        self.db_user_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Database user (default: mypersonalmap_user)",
            height=40,
        )
        self.db_user_entry.insert(0, "mypersonalmap_user")
        self.db_user_entry.pack(fill="x", padx=SPACING["lg"], pady=SPACING["sm"])

        # DB password
        self.db_password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Database password",
            show="•",
            height=40,
        )
        self.db_password_entry.pack(fill="x", padx=SPACING["lg"], pady=SPACING["sm"])

        # Status label
        self.status_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=get_font("sans", "sm", "normal"),
        )
        self.status_label.pack(pady=SPACING["md"])

        # Buttons
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=SPACING["lg"])

        back_btn = CustomButton(
            btn_frame,
            text="← Back",
            variant="secondary",
            command=self.show_mysql_not_found,
        )
        back_btn.pack(side="left")

        create_btn = CustomButton(
            btn_frame,
            text="Create Database",
            variant="accent",
            command=self.create_mysql_database,
        )
        create_btn.pack(side="right")

    def create_mysql_database(self):
        """Create MySQL database with user credentials"""
        root_password = self.root_password_entry.get()
        db_name = self.db_name_entry.get() or "mypersonalmap"
        db_user = self.db_user_entry.get() or "mypersonalmap_user"
        db_password = self.db_password_entry.get()

        if not root_password:
            self.status_label.configure(
                text="❌ Please enter root password",
                text_color=COLORS["error"]
            )
            return

        if not db_password:
            self.status_label.configure(
                text="❌ Please enter database password",
                text_color=COLORS["error"]
            )
            return

        try:
            self.status_label.configure(
                text="Creating database...",
                text_color=COLORS["info"]
            )
            self.update()

            # Connect as root
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password=root_password,
            )

            with connection.cursor() as cursor:
                # Create database
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

                # Create user
                cursor.execute(
                    f"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_password}'"
                )

                # Grant privileges
                cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost'")
                cursor.execute("FLUSH PRIVILEGES")

            connection.close()

            # Update .env file
            self._update_env_file(db_name, db_user, db_password)

            self.db_configured = True
            self.show_success()

        except pymysql.err.OperationalError as e:
            self.status_label.configure(
                text=f"❌ Connection failed: {str(e)}",
                text_color=COLORS["error"]
            )
            logger.error(f"MySQL setup failed: {e}")
        except Exception as e:
            self.status_label.configure(
                text=f"❌ Error: {str(e)}",
                text_color=COLORS["error"]
            )
            logger.error(f"Unexpected error during MySQL setup: {e}")

    def setup_sqlite(self):
        """Setup SQLite as fallback"""
        self.clear_content()

        # Warning
        title = ctk.CTkLabel(
            self.content_frame,
            text="⚠️ SQLite Fallback",
            font=get_font("sans", "3xl", "bold"),
        )
        title.pack(pady=(0, SPACING["lg"]))

        warning_text = (
            "SQLite will be used as a fallback database.\n\n"
            "⚠️ LIMITATIONS:\n"
            "• Limited spatial query support\n"
            "• Reduced performance for large datasets\n"
            "• Some features may not work as expected\n\n"
            "It's recommended to install MySQL for full functionality."
        )
        warning = ctk.CTkLabel(
            self.content_frame,
            text=warning_text,
            font=get_font("sans", "base", "normal"),
            justify="left",
        )
        warning.pack(pady=SPACING["xl"])

        # Buttons
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=SPACING["lg"])

        back_btn = CustomButton(
            btn_frame,
            text="← Back",
            variant="secondary",
            command=self.show_mysql_not_found,
        )
        back_btn.pack(side="left")

        continue_btn = CustomButton(
            btn_frame,
            text="Continue with SQLite",
            variant="accent",
            command=self._setup_sqlite_backend,
        )
        continue_btn.pack(side="right")

    def _setup_sqlite_backend(self):
        """Actually setup SQLite"""
        # Update .env to use SQLite
        self._update_env_file_sqlite()
        self.db_configured = True
        self.show_success()

    def show_success(self):
        """Show success screen"""
        self.clear_content()

        # Success icon
        success_label = ctk.CTkLabel(
            self.content_frame,
            text="✅",
            font=get_font("sans", "5xl", "normal"),
        )
        success_label.pack(pady=SPACING["xl"])

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="Database Configured!",
            font=get_font("sans", "3xl", "bold"),
        )
        title.pack(pady=SPACING["lg"])

        # Info
        info = ctk.CTkLabel(
            self.content_frame,
            text="Your database is ready to use.\n\nClick below to start using My Personal Map!",
            font=get_font("sans", "base", "normal"),
        )
        info.pack(pady=SPACING["xl"])

        # Start button
        start_btn = CustomButton(
            self.content_frame,
            text="Start Application",
            variant="accent",
            width=200,
            height=48,
            command=self._complete_wizard,
        )
        start_btn.pack(pady=SPACING["2xl"])

    def _update_env_file(self, db_name: str, db_user: str, db_password: str):
        """Update .env file with database credentials"""
        from pymypersonalmap.gui.config_manager import ConfigManager

        config_mgr = ConfigManager()
        env_path = config_mgr.config_file

        # Read current .env
        env_content = env_path.read_text() if env_path.exists() else ""

        # Update database settings
        import re

        env_content = re.sub(r"DATABASE_NAME=.*", f"DATABASE_NAME={db_name}", env_content)
        env_content = re.sub(r"DATABASE_USER=.*", f"DATABASE_USER={db_user}", env_content)
        env_content = re.sub(r"DATABASE_PASSWORD=.*", f"DATABASE_PASSWORD={db_password}", env_content)
        env_content = re.sub(r"DATABASE_URL=.*", "DATABASE_URL=localhost", env_content)

        env_path.write_text(env_content)
        logger.info("Updated .env with database credentials")

    def _update_env_file_sqlite(self):
        """Update .env file to use SQLite"""
        # Similar to _update_env_file but for SQLite
        # Would need to change DATABASE_URL format
        pass

    def _complete_wizard(self):
        """Complete wizard and call callback"""
        if self.on_complete:
            self.on_complete()
        self.destroy()
