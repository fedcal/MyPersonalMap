"""
Splash Screen

Loading screen shown during application startup.
Displays branding, loading messages, and progress bar.
"""

import customtkinter as ctk
from pymypersonalmap.gui.theme import COLORS, SPACING, get_font


class SplashScreen(ctk.CTkToplevel):
    """
    Splash screen displayed during app initialization

    Features:
        - App branding and logo
        - Loading status message
        - Animated progress bar
        - Auto-close when app is ready

    Example:
        splash = SplashScreen(root)
        splash.update_message("Loading backend...")
        splash.update_progress(0.5)
        # When ready:
        splash.close()
    """

    def __init__(self, master=None, **kwargs):
        """
        Initialize splash screen

        Args:
            master: Parent widget (can be None for toplevel)
            **kwargs: Additional kwargs for CTkToplevel
        """
        super().__init__(master, **kwargs)

        # Window configuration
        self.title("")  # No title
        self.geometry("500x400")
        self.resizable(False, False)

        # Remove window decorations
        self.overrideredirect(True)

        # Center on screen
        self._center_window()

        # Configure style
        self.configure(fg_color=COLORS["gray_50"])

        # Create content
        self._create_content()

        # Bring to front
        self.lift()
        self.attributes("-topmost", True)

        # Initialize progress
        self._progress = 0.0
        self._message = "Inizializzazione..."

    def _center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = 500
        height = 400
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_content(self):
        """Create splash screen content"""
        # Main container
        container = ctk.CTkFrame(
            self,
            fg_color=COLORS["gray_50"],
            corner_radius=0,
        )
        container.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["xl"])

        # Logo/Icon section
        logo_frame = ctk.CTkFrame(container, fg_color="transparent")
        logo_frame.pack(pady=(SPACING["4xl"], SPACING["2xl"]))

        # Large map icon
        icon_label = ctk.CTkLabel(
            logo_frame,
            text="🗺️",
            font=get_font("sans", "5xl", "normal"),
        )
        icon_label.pack()

        # App name
        title_label = ctk.CTkLabel(
            logo_frame,
            text="My Personal Map",
            font=get_font("sans", "3xl", "bold"),
            text_color=COLORS["gray_900"],
        )
        title_label.pack(pady=(SPACING["md"], 0))

        # Version
        version_label = ctk.CTkLabel(
            logo_frame,
            text="v1.0.0",
            font=get_font("sans", "sm", "normal"),
            text_color=COLORS["gray_500"],
        )
        version_label.pack(pady=(SPACING["xs"], 0))

        # Spacer
        spacer = ctk.CTkFrame(container, fg_color="transparent", height=SPACING["2xl"])
        spacer.pack()

        # Loading message
        self.message_label = ctk.CTkLabel(
            container,
            text=self._message,
            font=get_font("sans", "base", "normal"),
            text_color=COLORS["gray_700"],
        )
        self.message_label.pack(pady=(0, SPACING["lg"]))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            container,
            width=400,
            height=8,
            corner_radius=4,
            fg_color=COLORS["gray_200"],
            progress_color=COLORS["primary"],
        )
        self.progress_bar.pack(pady=(0, SPACING["xl"]))
        self.progress_bar.set(0)

        # Footer text
        footer_label = ctk.CTkLabel(
            container,
            text="Gestisci le tue mappe personalizzate",
            font=get_font("sans", "sm", "normal"),
            text_color=COLORS["gray_500"],
        )
        footer_label.pack(side="bottom", pady=(SPACING["xl"], 0))

    def update_message(self, message: str):
        """
        Update loading message

        Args:
            message: New loading message to display
        """
        self._message = message
        if hasattr(self, "message_label"):
            self.message_label.configure(text=message)
            self.update()

    def update_progress(self, progress: float):
        """
        Update progress bar

        Args:
            progress: Progress value between 0.0 and 1.0
        """
        self._progress = max(0.0, min(1.0, progress))
        if hasattr(self, "progress_bar"):
            self.progress_bar.set(self._progress)
            self.update()

    def set_progress_with_message(self, progress: float, message: str):
        """
        Update both progress and message

        Args:
            progress: Progress value between 0.0 and 1.0
            message: New loading message
        """
        self.update_message(message)
        self.update_progress(progress)

    def close(self):
        """Close splash screen"""
        self.destroy()


class SplashScreenDark(SplashScreen):
    """
    Dark mode variant of splash screen

    Same functionality but with dark color scheme.
    """

    def _create_content(self):
        """Create splash screen content with dark colors"""
        # Override colors for dark mode
        bg_color = COLORS["dark_900"]
        text_primary = COLORS["dark_200"]
        text_secondary = COLORS["dark_400"]

        self.configure(fg_color=bg_color)

        # Main container
        container = ctk.CTkFrame(
            self,
            fg_color=bg_color,
            corner_radius=0,
        )
        container.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["xl"])

        # Logo/Icon section
        logo_frame = ctk.CTkFrame(container, fg_color="transparent")
        logo_frame.pack(pady=(SPACING["4xl"], SPACING["2xl"]))

        # Large map icon
        icon_label = ctk.CTkLabel(
            logo_frame,
            text="🗺️",
            font=get_font("sans", "5xl", "normal"),
        )
        icon_label.pack()

        # App name
        title_label = ctk.CTkLabel(
            logo_frame,
            text="My Personal Map",
            font=get_font("sans", "3xl", "bold"),
            text_color=text_primary,
        )
        title_label.pack(pady=(SPACING["md"], 0))

        # Version
        version_label = ctk.CTkLabel(
            logo_frame,
            text="v1.0.0",
            font=get_font("sans", "sm", "normal"),
            text_color=text_secondary,
        )
        version_label.pack(pady=(SPACING["xs"], 0))

        # Spacer
        spacer = ctk.CTkFrame(container, fg_color="transparent", height=SPACING["2xl"])
        spacer.pack()

        # Loading message
        self.message_label = ctk.CTkLabel(
            container,
            text=self._message,
            font=get_font("sans", "base", "normal"),
            text_color=text_primary,
        )
        self.message_label.pack(pady=(0, SPACING["lg"]))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            container,
            width=400,
            height=8,
            corner_radius=4,
            fg_color=COLORS["dark_700"],
            progress_color=COLORS["primary"],
        )
        self.progress_bar.pack(pady=(0, SPACING["xl"]))
        self.progress_bar.set(0)

        # Footer text
        footer_label = ctk.CTkLabel(
            container,
            text="Gestisci le tue mappe personalizzate",
            font=get_font("sans", "sm", "normal"),
            text_color=text_secondary,
        )
        footer_label.pack(side="bottom", pady=(SPACING["xl"], 0))
