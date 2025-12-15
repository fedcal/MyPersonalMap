"""
Theme Configuration for My Personal Map GUI

Provides centralized theme management for CustomTkinter components
following the design system defined in DESIGN_SYSTEM.md
"""

import customtkinter as ctk
from pathlib import Path

# Path to theme JSON file
THEME_PATH = Path(__file__).parent / "themes" / "mypersonalmap_theme.json"

# Design System Colors (from DESIGN_SYSTEM.md)
COLORS = {
    # Primary Colors
    "primary": "#4F46E5",
    "primary_light": "#818CF8",
    "primary_dark": "#3730A3",
    "secondary": "#9333EA",
    "accent": "#F59E0B",

    # Semantic Colors
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#06B6D4",

    # Light Mode Neutrals
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",

    # Dark Mode Neutrals
    "dark_900": "#0F172A",
    "dark_800": "#1E293B",
    "dark_700": "#334155",
    "dark_600": "#475569",
    "dark_500": "#64748B",
    "dark_400": "#94A3B8",
    "dark_300": "#CBD5E1",
    "dark_200": "#E2E8F0",
    "dark_100": "#F1F5F9",
}

# Spacing Scale (4px base unit)
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "2xl": 48,
    "3xl": 64,
    "4xl": 96,
}

# Font Families
FONTS = {
    "sans": ("Inter", "Segoe UI", "Helvetica", "Arial", "sans-serif"),
    "mono": ("JetBrains Mono", "Fira Code", "Courier New", "monospace"),
}

# Font Sizes (pixels)
FONT_SIZES = {
    "xs": 12,
    "sm": 14,
    "base": 16,
    "lg": 18,
    "xl": 20,
    "2xl": 24,
    "3xl": 30,
    "4xl": 36,
    "5xl": 48,
}

# Border Radius
RADIUS = {
    "sm": 4,
    "md": 6,
    "lg": 8,
    "xl": 12,
    "2xl": 16,
    "full": 9999,
}


def init_theme(mode="dark"):
    """
    Initialize CustomTkinter theme

    Args:
        mode: "light" or "dark" (default: "dark")
    """
    # Set appearance mode
    ctk.set_appearance_mode(mode)

    # Set theme
    if THEME_PATH.exists():
        ctk.set_default_color_theme(str(THEME_PATH))
    else:
        # Fallback to default theme if custom theme not found
        ctk.set_default_color_theme("blue")


def get_font(family="sans", size="base", weight="normal"):
    """
    Get font tuple for CustomTkinter widgets

    Args:
        family: "sans" or "mono"
        size: Size key from FONT_SIZES
        weight: "normal" or "bold"

    Returns:
        Tuple (font_name, size, weight)
    """
    font_name = FONTS.get(family, FONTS["sans"])[0]
    font_size = FONT_SIZES.get(size, FONT_SIZES["base"])

    return (font_name, font_size, weight)


def get_color(color_key, mode="dark"):
    """
    Get color value by key

    Args:
        color_key: Key from COLORS dict
        mode: "light" or "dark" (for context-specific colors)

    Returns:
        Hex color string
    """
    return COLORS.get(color_key, COLORS["gray_500"])


# Predefined font configurations
FONT_HEADING = get_font("sans", "3xl", "bold")
FONT_SUBHEADING = get_font("sans", "xl", "bold")
FONT_BODY = get_font("sans", "base", "normal")
FONT_SMALL = get_font("sans", "sm", "normal")
FONT_MONO = get_font("mono", "base", "normal")
