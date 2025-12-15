"""
Error Handler for GUI

Centralized error handling with user-friendly dialogs and logging.
"""

import customtkinter as ctk
import logging
import traceback
from typing import Optional, Callable
from pymypersonalmap.gui.theme import COLORS, SPACING, get_font


logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    Centralized error handler for GUI applications

    Provides user-friendly error dialogs with:
    - Clear error messages
    - Actionable buttons (Retry, Ignore, Exit)
    - Collapsible technical details (in DEBUG mode)
    - Automatic logging

    Example:
        try:
            risky_operation()
        except Exception as e:
            ErrorHandler.handle_exception(
                parent_widget, e,
                context="Failed to save marker",
                retry_callback=lambda: risky_operation()
            )
    """

    @staticmethod
    def handle_exception(
        parent: ctk.CTk,
        error: Exception,
        context: str,
        retry_callback: Optional[Callable] = None,
        show_exit: bool = False
    ):
        """
        Show error dialog with user-friendly message

        Args:
            parent: Parent widget for dialog
            error: Exception that occurred
            context: Context description (e.g., "Failed to save marker")
            retry_callback: Optional callback for Retry button
            show_exit: If True, show Exit button instead of Close
        """
        # Log error with full traceback
        logger.error(f"{context}: {str(error)}", exc_info=True)

        # Get user-friendly message
        user_message = ErrorHandler._get_user_message(error, context)

        # Create error dialog
        ErrorHandler._show_error_dialog(
            parent,
            user_message,
            error,
            context,
            retry_callback,
            show_exit
        )

    @staticmethod
    def _get_user_message(error: Exception, context: str) -> str:
        """
        Convert technical error to user-friendly message

        Args:
            error: Exception object
            context: Context description

        Returns:
            User-friendly error message
        """
        error_type = type(error).__name__
        error_str = str(error)

        # Common error patterns with user-friendly messages
        error_mappings = {
            "FileNotFoundError": f"File non trovato. {error_str}",
            "PermissionError": f"Permessi insufficienti per accedere al file.",
            "ConnectionError": f"Errore di connessione. Verifica la connessione di rete.",
            "TimeoutError": f"Operazione timeout. Riprova più tardi.",
            "ValueError": f"Valore non valido: {error_str}",
            "KeyError": f"Chiave mancante: {error_str}",
            "AttributeError": f"Attributo non trovato: {error_str}",
        }

        # Check for pymysql errors
        if "pymysql" in error_type.lower() or "OperationalError" in error_type:
            if "1045" in error_str:
                return "Password MySQL non corretta"
            elif "2003" in error_str:
                return "Impossibile connettersi al server MySQL. È in esecuzione?"
            elif "1049" in error_str:
                return f"Database non trovato"
            else:
                return f"Errore database: {error_str}"

        # Check for network errors
        if "ConnectionRefusedError" in error_type:
            return "Connessione rifiutata. Il server non è raggiungibile."

        # Try to find mapping
        for err_type, message in error_mappings.items():
            if err_type in error_type:
                return message

        # Default message
        return f"{context}\n\nDettagli: {error_str}"

    @staticmethod
    def _show_error_dialog(
        parent: ctk.CTk,
        user_message: str,
        error: Exception,
        context: str,
        retry_callback: Optional[Callable],
        show_exit: bool
    ):
        """
        Create and show error dialog window

        Args:
            parent: Parent widget
            user_message: User-friendly message
            error: Original exception
            context: Context description
            retry_callback: Optional retry callback
            show_exit: Show exit button
        """
        # Create dialog
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Errore")
        dialog.geometry("500x400")
        dialog.resizable(False, False)

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 200
        dialog.geometry(f"+{x}+{y}")

        # Make modal
        dialog.transient(parent)
        dialog.grab_set()

        # Content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["xl"])

        # Error icon
        icon_label = ctk.CTkLabel(
            content_frame,
            text="❌",
            font=("Arial", 48),
        )
        icon_label.pack(pady=(0, SPACING["lg"]))

        # User message
        message_label = ctk.CTkLabel(
            content_frame,
            text=user_message,
            font=get_font("sans", "base", "normal"),
            wraplength=450,
            justify="center",
        )
        message_label.pack(pady=SPACING["md"])

        # Technical details (collapsible)
        from pymypersonalmap.config.settings import DEBUG
        if DEBUG:
            details_frame = ctk.CTkFrame(content_frame)
            details_frame.pack(fill="both", expand=True, pady=SPACING["md"])

            details_label = ctk.CTkLabel(
                details_frame,
                text="Dettagli Tecnici:",
                font=get_font("sans", "sm", "bold"),
                anchor="w",
            )
            details_label.pack(fill="x", padx=SPACING["sm"], pady=(SPACING["sm"], 0))

            details_text = ctk.CTkTextbox(
                details_frame,
                height=100,
                font=get_font("mono", "xs", "normal"),
            )
            details_text.pack(fill="both", expand=True, padx=SPACING["sm"], pady=SPACING["sm"])

            # Insert error details
            error_details = f"{context}\n\nType: {type(error).__name__}\n\n{traceback.format_exc()}"
            details_text.insert("1.0", error_details)
            details_text.configure(state="disabled")

        # Buttons frame
        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(SPACING["lg"], 0))

        # Retry button (if callback provided)
        if retry_callback:
            retry_btn = ctk.CTkButton(
                btn_frame,
                text="🔄 Riprova",
                command=lambda: [dialog.destroy(), retry_callback()],
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"],
                width=120,
                height=40,
            )
            retry_btn.pack(side="left", padx=SPACING["sm"])

        # Close/Exit button
        close_text = "❌ Esci" if show_exit else "✓ Chiudi"
        close_command = lambda: [dialog.destroy(), parent.quit()] if show_exit else dialog.destroy

        close_btn = ctk.CTkButton(
            btn_frame,
            text=close_text,
            command=close_command,
            fg_color=COLORS["gray_600"] if not show_exit else COLORS["error"],
            hover_color=COLORS["gray_700"] if not show_exit else COLORS["error"],
            width=120,
            height=40,
        )
        close_btn.pack(side="right", padx=SPACING["sm"])

        # Ignore button (center, if retry is available)
        if retry_callback and not show_exit:
            ignore_btn = ctk.CTkButton(
                btn_frame,
                text="⊘ Ignora",
                command=dialog.destroy,
                fg_color=COLORS["gray_500"],
                hover_color=COLORS["gray_600"],
                width=120,
                height=40,
            )
            ignore_btn.pack(side="left", padx=SPACING["sm"])

    @staticmethod
    def show_warning(parent: ctk.CTk, message: str, title: str = "Attenzione"):
        """
        Show warning dialog

        Args:
            parent: Parent widget
            message: Warning message
            title: Dialog title
        """
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry("400x250")

        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 125
        dialog.geometry(f"+{x}+{y}")

        # Content
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["xl"])

        # Icon
        icon = ctk.CTkLabel(content, text="⚠️", font=("Arial", 48))
        icon.pack(pady=(0, SPACING["lg"]))

        # Message
        msg = ctk.CTkLabel(
            content,
            text=message,
            font=get_font("sans", "base", "normal"),
            wraplength=350,
            justify="center",
        )
        msg.pack(pady=SPACING["md"])

        # OK button
        ok_btn = ctk.CTkButton(
            content,
            text="OK",
            command=dialog.destroy,
            fg_color=COLORS["warning"],
            width=120,
            height=40,
        )
        ok_btn.pack(pady=SPACING["lg"])

    @staticmethod
    def show_info(parent: ctk.CTk, message: str, title: str = "Informazione"):
        """
        Show info dialog

        Args:
            parent: Parent widget
            message: Info message
            title: Dialog title
        """
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry("400x250")

        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 125
        dialog.geometry(f"+{x}+{y}")

        # Content
        content = ctk.CTkFrame(dialog, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["xl"])

        # Icon
        icon = ctk.CTkLabel(content, text="ℹ️", font=("Arial", 48))
        icon.pack(pady=(0, SPACING["lg"]))

        # Message
        msg = ctk.CTkLabel(
            content,
            text=message,
            font=get_font("sans", "base", "normal"),
            wraplength=350,
            justify="center",
        )
        msg.pack(pady=SPACING["md"])

        # OK button
        ok_btn = ctk.CTkButton(
            content,
            text="OK",
            command=dialog.destroy,
            fg_color=COLORS["info"],
            width=120,
            height=40,
        )
        ok_btn.pack(pady=SPACING["lg"])
