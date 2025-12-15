"""
Custom Button Components

Provides styled buttons following the design system:
- Primary: Main actions
- Secondary: Secondary actions
- Accent: Call-to-action buttons
"""

import customtkinter as ctk
from pymypersonalmap.gui.theme import COLORS, RADIUS, get_font


class CustomButton(ctk.CTkButton):
    """
    Base button component following design system

    Variants:
        - primary: Main brand color (default)
        - secondary: Transparent with border
        - accent: Accent color for CTAs
        - success: Success actions
        - error: Destructive actions
    """

    def __init__(self, master, variant="primary", **kwargs):
        # Variant styles
        styles = {
            "primary": {
                "fg_color": COLORS["primary"],
                "hover_color": COLORS["primary_dark"],
                "text_color": "#FFFFFF",
                "border_width": 0,
            },
            "secondary": {
                "fg_color": "transparent",
                "border_color": COLORS["primary"],
                "border_width": 1,
                "text_color": COLORS["primary"],
                "hover_color": COLORS["gray_100"],
            },
            "accent": {
                "fg_color": COLORS["accent"],
                "hover_color": "#D97706",  # Darker accent
                "text_color": "#FFFFFF",
                "border_width": 0,
            },
            "success": {
                "fg_color": COLORS["success"],
                "hover_color": "#059669",  # Darker success
                "text_color": "#FFFFFF",
                "border_width": 0,
            },
            "error": {
                "fg_color": COLORS["error"],
                "hover_color": "#DC2626",  # Darker error
                "text_color": "#FFFFFF",
                "border_width": 0,
            },
        }

        # Get style for variant
        style = styles.get(variant, styles["primary"])

        # Merge with user kwargs (user kwargs override defaults)
        kwargs = {
            "corner_radius": RADIUS["md"],
            "font": get_font("sans", "base", "normal"),
            "height": 36,
            **style,
            **kwargs,
        }

        super().__init__(master, **kwargs)


class IconButton(CustomButton):
    """
    Button with icon (using Unicode symbols or emoji)

    Example:
        IconButton(parent, icon="➕", text="Add Marker", variant="accent")
    """

    def __init__(self, master, icon="", **kwargs):
        text = kwargs.pop("text", "")
        if icon and text:
            display_text = f"{icon}  {text}"
        elif icon:
            display_text = icon
        else:
            display_text = text

        super().__init__(master, text=display_text, **kwargs)
