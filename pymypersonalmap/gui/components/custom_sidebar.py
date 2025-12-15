"""
Custom Sidebar Component

Navigation sidebar for the application with menu items,
quick actions, and user info.
"""

import customtkinter as ctk
from pymypersonalmap.gui.theme import COLORS, SPACING, get_font
from pymypersonalmap.gui.components.custom_button import CustomButton


class Sidebar(ctk.CTkFrame):
    """
    Navigation sidebar component

    Features:
        - App branding/logo
        - Navigation menu
        - Quick actions
        - Settings/user menu
    """

    def __init__(self, master, width=280, **kwargs):
        """
        Initialize Sidebar

        Args:
            master: Parent widget
            width: Sidebar width in pixels (default: 280)
            **kwargs: Additional kwargs for CTkFrame
        """
        super().__init__(master, width=width, **kwargs)

        # Prevent sidebar from shrinking
        self.pack_propagate(False)

        # Branding section
        self._create_branding()

        # Navigation menu
        self._create_navigation()

        # Spacer
        ctk.CTkFrame(self, fg_color="transparent", height=SPACING["xl"]).pack()

        # Quick actions
        self._create_quick_actions()

        # Bottom section (settings, user)
        self._create_bottom_section()

    def _create_branding(self):
        """Create app branding/logo section"""
        brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        brand_frame.pack(fill="x", padx=SPACING["lg"], pady=SPACING["xl"])

        # App icon/emoji
        icon_label = ctk.CTkLabel(
            brand_frame,
            text="🗺️",
            font=get_font("sans", "5xl", "normal"),
        )
        icon_label.pack()

        # App title
        title_label = ctk.CTkLabel(
            brand_frame,
            text="My Personal Map",
            font=get_font("sans", "xl", "bold"),
        )
        title_label.pack(pady=(SPACING["sm"], 0))

        # Divider
        divider = ctk.CTkFrame(brand_frame, height=1, fg_color=COLORS["gray_300"])
        divider.pack(fill="x", pady=SPACING["lg"])

    def _create_navigation(self):
        """Create navigation menu items"""
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=SPACING["md"])

        # Menu items
        menu_items = [
            {"icon": "🗺️", "text": "Mappa", "command": None},
            {"icon": "📍", "text": "Markers", "command": None},
            {"icon": "🏷️", "text": "Etichette", "command": None},
            {"icon": "🛣️", "text": "Percorsi", "command": None},
            {"icon": "📊", "text": "Statistiche", "command": None},
        ]

        for item in menu_items:
            btn = NavButton(
                nav_frame,
                icon=item["icon"],
                text=item["text"],
                command=item["command"],
            )
            btn.pack(fill="x", pady=SPACING["xs"])

    def _create_quick_actions(self):
        """Create quick action buttons"""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=SPACING["lg"])

        # Section title
        title = ctk.CTkLabel(
            actions_frame,
            text="Azioni Rapide",
            font=get_font("sans", "sm", "bold"),
            anchor="w",
        )
        title.pack(fill="x", pady=(0, SPACING["sm"]))

        # Quick action buttons
        add_marker_btn = CustomButton(
            actions_frame,
            text="➕ Nuovo Marker",
            variant="accent",
            command=None,
        )
        add_marker_btn.pack(fill="x", pady=SPACING["xs"])

        import_btn = CustomButton(
            actions_frame,
            text="📥 Importa GPX",
            variant="secondary",
            command=None,
        )
        import_btn.pack(fill="x", pady=SPACING["xs"])

    def _create_bottom_section(self):
        """Create bottom section with settings and user menu"""
        # Spacer to push bottom section down
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        # Bottom frame
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=SPACING["lg"], pady=SPACING["lg"])

        # Divider
        divider = ctk.CTkFrame(bottom_frame, height=1, fg_color=COLORS["gray_300"])
        divider.pack(fill="x", pady=(0, SPACING["md"]))

        # Settings button
        settings_btn = NavButton(
            bottom_frame,
            icon="⚙️",
            text="Impostazioni",
            command=None,
        )
        settings_btn.pack(fill="x", pady=SPACING["xs"])

        # User/profile button
        user_btn = NavButton(
            bottom_frame,
            icon="👤",
            text="Profilo",
            command=None,
        )
        user_btn.pack(fill="x", pady=SPACING["xs"])


class NavButton(ctk.CTkButton):
    """
    Navigation menu button

    Styled button for sidebar navigation
    """

    def __init__(self, master, icon="", text="", **kwargs):
        display_text = f"{icon}  {text}" if icon else text

        kwargs = {
            "text": display_text,
            "fg_color": "transparent",
            "text_color": COLORS["gray_700"],
            "hover_color": COLORS["gray_200"],
            "anchor": "w",
            "height": 40,
            "corner_radius": SPACING["sm"],
            "font": get_font("sans", "base", "normal"),
            **kwargs,
        }

        super().__init__(master, **kwargs)
