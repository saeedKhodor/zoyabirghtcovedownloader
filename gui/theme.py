# === CODE INDEX ===
# is_macos()                               Line 14
# get_system_font(size, weight)            Line 20
# setup_custom_theme(root)                 Line 36

"""
macOS-native styled theme configuration for Tkinter ttk.
Provides clean modern typography, macOS Aqua integration, and cross-platform palette.
"""

import sys
import tkinter as tk
from tkinter import ttk


def is_macos() -> bool:
    """Returns True if the current platform is macOS."""
    return sys.platform == "darwin"


def get_system_font(size: int = 12, weight: str = "normal") -> tuple:
    """Returns the most appropriate system font family based on OS."""
    if is_macos():
        family = ".AppleSystemUIFont"
    else:
        family = "Segoe UI"
    return (family, size, weight)


# Color palette inspired by Apple Human Interface Guidelines
COLORS = {
    "bg": "#F5F5F7" if not is_macos() else "systemWindowBackgroundColor",
    "card_bg": "#FFFFFF",
    "card_border": "#E5E5EA",
    "primary": "#007AFF",
    "primary_hover": "#0062CC",
    "primary_text": "#FFFFFF",
    "text": "#1D1D1F",
    "text_secondary": "#6E6E73",
    "success": "#34C759",
    "danger": "#FF3B30",
    "log_bg": "#1E1E1E",
    "log_text": "#E0E0E0",
}


def setup_custom_theme(root: tk.Tk):
    """Configures modern ttk styles and widget appearances."""
    style = ttk.Style(root)

    # Use native theme as base ('aqua' on macOS, 'clam' on Windows/Linux)
    available_themes = style.theme_names()
    if is_macos() and "aqua" in available_themes:
        style.theme_use("aqua")
    elif "clam" in available_themes:
        style.theme_use("clam")

    # Font definitions
    regular_font = get_system_font(12)
    bold_font = get_system_font(12, "bold")
    header_font = get_system_font(16, "bold")
    small_font = get_system_font(10)

    # Configure styles
    style.configure(".", font=regular_font)
    style.configure("Title.TLabel", font=header_font, foreground="#1D1D1F")
    style.configure("Subtitle.TLabel", font=small_font, foreground="#6E6E73")
    style.configure("FieldLabel.TLabel", font=bold_font, foreground="#1D1D1F")
    style.configure("Helper.TLabel", font=small_font, foreground="#8E8E93")
    style.configure("Status.TLabel", font=regular_font, foreground="#1D1D1F")

    # Accent button style
    if not is_macos():
        style.configure(
            "Primary.TButton",
            font=bold_font,
            background=COLORS["primary"],
            foreground=COLORS["primary_text"],
            padding=8,
        )
        style.map(
            "Primary.TButton",
            background=[("active", COLORS["primary_hover"]), ("disabled", "#CCCCCC")],
        )
