"""
Map Viewer Component

Embeds Folium interactive maps in CustomTkinter using tkinterweb.
This is the core component for displaying geographic markers.
"""

import customtkinter as ctk
from tkinterweb import HtmlFrame
import folium
import tempfile
import logging
from pathlib import Path
from typing import List, Tuple, Optional
from pymypersonalmap.gui.error_handler import ErrorHandler


logger = logging.getLogger(__name__)


class MapViewer(ctk.CTkFrame):
    """
    Folium map viewer embedded in CustomTkinter

    Features:
        - Interactive Leaflet map via Folium
        - Add/remove markers dynamically
        - Zoom controls
        - Pan and navigate

    Example:
        map_viewer = MapViewer(parent, center=(45.46, 9.19), zoom=12)
        map_viewer.add_marker(lat=45.46, lon=9.19, popup="Milano", color="blue")
        map_viewer.render()
    """

    def __init__(
        self,
        master,
        center: Tuple[float, float] = (45.4642, 9.1900),
        zoom: int = 12,
        **kwargs
    ):
        """
        Initialize MapViewer

        Args:
            master: Parent widget
            center: Tuple (latitude, longitude) for initial center
            zoom: Initial zoom level (1-18)
            **kwargs: Additional kwargs for CTkFrame
        """
        super().__init__(master, **kwargs)

        # HTML renderer
        self.webview = HtmlFrame(self, messages_enabled=False)
        self.webview.pack(fill="both", expand=True)

        # Folium map
        self.map = None
        self.markers = []
        self.temp_file = None
        self.center = center
        self.zoom = zoom

        # Initialize map
        self.init_map(center=center, zoom=zoom)

    def init_map(self, center: Tuple[float, float], zoom: int):
        """
        Initialize Folium map

        Args:
            center: Tuple (latitude, longitude)
            zoom: Zoom level
        """
        self.map = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles="OpenStreetMap",
            control_scale=True,
        )

        # Add fullscreen control
        folium.plugins.Fullscreen(
            position="topleft",
            title="Fullscreen",
            title_cancel="Exit fullscreen",
        ).add_to(self.map)

        # Render initial map
        self.render()

    def add_marker(
        self,
        lat: float,
        lon: float,
        popup_text: str = "",
        icon_color: str = "blue",
        icon_symbol: str = "info-sign",
        tooltip: Optional[str] = None,
    ):
        """
        Add marker to the map

        Args:
            lat: Latitude
            lon: Longitude
            popup_text: Text to show in popup
            icon_color: Marker color (blue, red, green, purple, orange, etc.)
            icon_symbol: Icon from Bootstrap/Font Awesome
            tooltip: Tooltip text on hover
        """
        marker = folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            tooltip=tooltip,
            icon=folium.Icon(color=icon_color, icon=icon_symbol, prefix="glyphicon"),
        )
        marker.add_to(self.map)
        self.markers.append(marker)

        # Re-render map
        self.render()

    def clear_markers(self):
        """Remove all markers from the map"""
        # Reinitialize map (Folium doesn't have remove marker method)
        self.init_map(center=self.center, zoom=self.zoom)
        self.markers = []

    def set_center(self, lat: float, lon: float, zoom: Optional[int] = None):
        """
        Set map center and optionally zoom

        Args:
            lat: Latitude
            lon: Longitude
            zoom: Optional zoom level
        """
        self.center = (lat, lon)
        if zoom is not None:
            self.zoom = zoom

        # Folium doesn't support dynamic center change, need to recreate
        # Save markers first
        old_markers = self.markers.copy()
        self.init_map(center=self.center, zoom=self.zoom)

        # Restore markers
        # Note: This is simplified - in production would need to restore all marker properties
        self.markers = old_markers
        for marker in self.markers:
            marker.add_to(self.map)

        self.render()

    def render(self):
        """
        Render Folium map in WebView

        Saves map to temporary HTML file and loads it in tkinterweb
        """
        # Clean up previous temp file
        if self.temp_file:
            try:
                Path(self.temp_file.name).unlink(missing_ok=True)
            except:
                pass

        # Create new temp file
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False
        )

        # Save map HTML
        self.map.save(self.temp_file.name)
        self.temp_file.flush()

        # Load in WebView
        self.webview.load_file(self.temp_file.name)

    def __del__(self):
        """Cleanup temporary file on deletion"""
        if self.temp_file:
            try:
                Path(self.temp_file.name).unlink(missing_ok=True)
            except:
                pass
