"""
Main Layout

Primary application layout with sidebar, top bar, and content area
"""

import customtkinter as ctk
from pymypersonalmap.gui.components import Sidebar, MapViewer
from pymypersonalmap.gui.theme import COLORS, SPACING, get_font


class MainLayout(ctk.CTkFrame):
    """
    Main application layout

    Structure:
        [Sidebar (280px)] [Content Area]
                              - Top Bar (64px)
                              - Main Content (map/list)
    """

    def __init__(self, master, **kwargs):
        """
        Initialize MainLayout

        Args:
            master: Parent widget
            **kwargs: Additional kwargs for CTkFrame
        """
        super().__init__(master, **kwargs)

        # Sidebar (fixed width 280px)
        self.sidebar = Sidebar(self, width=280)
        self.sidebar.pack(side="left", fill="y")

        # Content area (right side)
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True)

        # Top bar
        self.topbar = self._create_topbar()
        self.topbar.pack(fill="x", padx=SPACING["md"], pady=SPACING["sm"])

        # Main content (map viewer by default)
        self.main_content = ctk.CTkFrame(
            self.content_area,
            fg_color="transparent"
        )
        self.main_content.pack(fill="both", expand=True, padx=SPACING["md"], pady=SPACING["sm"])

        # Initialize map viewer
        self.map_viewer = MapViewer(
            self.main_content,
            center=(45.4642, 9.1900),  # Milan, Italy default
            zoom=12
        )
        self.map_viewer.pack(fill="both", expand=True)

    def _create_topbar(self):
        """
        Create top bar with search and user menu

        Returns:
            CTkFrame: Top bar frame
        """
        topbar = ctk.CTkFrame(
            self.content_area,
            height=64,
            fg_color=COLORS["gray_100"],
            corner_radius=SPACING["sm"]
        )

        # Prevent topbar from shrinking
        topbar.pack_propagate(False)

        # Left section - Title/breadcrumb
        left_section = ctk.CTkFrame(topbar, fg_color="transparent")
        left_section.pack(side="left", padx=SPACING["lg"], pady=SPACING["md"])

        title_label = ctk.CTkLabel(
            left_section,
            text="Mappa",
            font=get_font("sans", "2xl", "bold"),
        )
        title_label.pack(side="left")

        # Middle section - Search (placeholder)
        middle_section = ctk.CTkFrame(topbar, fg_color="transparent")
        middle_section.pack(side="left", expand=True, fill="x", padx=SPACING["xl"])

        search_entry = ctk.CTkEntry(
            middle_section,
            placeholder_text="Cerca marker, luoghi...",
            width=400,
            height=36,
        )
        search_entry.pack(side="left", padx=SPACING["md"])

        # Right section - Actions
        right_section = ctk.CTkFrame(topbar, fg_color="transparent")
        right_section.pack(side="right", padx=SPACING["lg"], pady=SPACING["md"])

        # View toggle (map/list) - placeholder
        view_label = ctk.CTkLabel(
            right_section,
            text="Vista: Mappa",
            font=get_font("sans", "sm", "normal"),
        )
        view_label.pack(side="left", padx=SPACING["md"])

        return topbar

    def show_map(self):
        """Switch to map view"""
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.pack_forget()

        # Show map viewer
        self.map_viewer.pack(fill="both", expand=True)

    def show_list(self):
        """Switch to list view (to be implemented)"""
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.pack_forget()

        # Placeholder for list view
        list_label = ctk.CTkLabel(
            self.main_content,
            text="List View - To be implemented",
            font=get_font("sans", "2xl", "normal"),
        )
        list_label.pack(expand=True)
