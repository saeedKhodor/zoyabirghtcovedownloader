# === CODE INDEX ===
# main()                                   Line 18

"""
Main Application Entry Point for Brightcove Video Downloader.
"""

import sys
import core.mac_patch  # Must be imported first to patch macOS platform version
import tkinter as tk
from gui.main_window import MainWindow


def main():
    """Initializes and runs the GUI main event loop."""
    # Enable high-DPI awareness on Windows if applicable
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
