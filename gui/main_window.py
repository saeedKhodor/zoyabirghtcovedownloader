# === CODE INDEX ===
# MainWindow.__init__                      Line 32
# MainWindow._init_ui                      Line 45
# MainWindow._create_header                Line 60
# MainWindow._create_input_fields          Line 77
# MainWindow._create_controls              Line 135
# MainWindow._create_progress_section      Line 160
# MainWindow._create_log_console           Line 180
# MainWindow._bind_shortcuts               Line 205
# MainWindow.start_download                Line 230
# MainWindow.cancel_download               Line 265
# MainWindow._on_progress                  Line 275
# MainWindow._on_status                    Line 285
# MainWindow._on_completion                Line 295
# MainWindow.open_output_folder            Line 320

"""
Main Application GUI Window for Brightcove Video Downloader.
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional

from core.downloader import BrightcoveDownloader
from core.url_builder import parse_input_fields
from gui.theme import setup_custom_theme, get_system_font, is_macos, COLORS


class MainWindow:
    """Main application window managing UI layout, thread dispatch, and user interactions."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Brightcove Video Downloader")
        self.root.geometry("640x700")
        self.root.minsize(580, 620)

        setup_custom_theme(self.root)

        # State tracking
        self.downloader: Optional[BrightcoveDownloader] = None
        self.download_thread: Optional[threading.Thread] = None
        self.is_downloading = False
        self.last_downloaded_file: Optional[str] = None

        self._init_ui()
        self._bind_shortcuts()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _init_ui(self):
        """Builds top-level container and child sections."""
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        self._create_header(container)
        self._create_input_fields(container)
        self._create_controls(container)
        self._create_progress_section(container)
        self._create_log_console(container)

    def _create_header(self, parent: ttk.Frame):
        """Header title and subtitle."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title = ttk.Label(
            header_frame,
            text="Brightcove Video Downloader",
            style="Title.TLabel",
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header_frame,
            text="Enter Account, Player, and Video IDs to download high quality video streams.",
            style="Subtitle.TLabel",
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    def _create_input_fields(self, parent: ttk.Frame):
        """Forms for Account ID, Player ID, Video ID, Output Dir, and Quality."""
        card = ttk.LabelFrame(parent, text=" Video Information ", padding=12)
        card.pack(fill=tk.X, pady=(0, 12))

        # Grid configuration
        card.columnconfigure(1, weight=1)

        # 1. Account ID
        ttk.Label(card, text="Account ID:", style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w", pady=4)
        self.account_entry = ttk.Entry(card, font=get_system_font(12))
        self.account_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=4)
        self.account_entry.insert(0, "3887645559001")

        # 2. Player ID
        ttk.Label(card, text="Player ID:", style="FieldLabel.TLabel").grid(row=1, column=0, sticky="w", pady=4)
        self.player_entry = ttk.Entry(card, font=get_system_font(12))
        self.player_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=4)
        self.player_entry.insert(0, "default")

        # 3. Video ID
        ttk.Label(card, text="Video ID:", style="FieldLabel.TLabel").grid(row=2, column=0, sticky="w", pady=4)
        self.video_entry = ttk.Entry(card, font=get_system_font(12))
        self.video_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=4)
        self.video_entry.insert(0, "5978804382001")

        # 4. Save Location
        default_dir = os.path.expanduser("~/Downloads")
        if not os.path.exists(default_dir):
            default_dir = os.path.expanduser("~")

        ttk.Label(card, text="Save To:", style="FieldLabel.TLabel").grid(row=3, column=0, sticky="w", pady=4)
        self.dir_var = tk.StringVar(value=default_dir)
        self.dir_entry = ttk.Entry(card, textvariable=self.dir_var, font=get_system_font(11))
        self.dir_entry.grid(row=3, column=1, sticky="ew", padx=(8, 4), pady=4)

        browse_btn = ttk.Button(card, text="Browse...", command=self._browse_directory)
        browse_btn.grid(row=3, column=2, sticky="e", pady=4)

        # 5. Quality selector
        ttk.Label(card, text="Quality:", style="FieldLabel.TLabel").grid(row=4, column=0, sticky="w", pady=4)
        self.quality_var = tk.StringVar(value="Best Available")
        quality_options = ["Best Available", "1080p", "720p", "480p", "Audio Only (M4A/MP3)"]
        self.quality_combo = ttk.Combobox(
            card,
            textvariable=self.quality_var,
            values=quality_options,
            state="readonly",
            font=get_system_font(11),
        )
        self.quality_combo.grid(row=4, column=1, sticky="w", padx=(8, 0), pady=4)

    def _browse_directory(self):
        """Opens native directory picker."""
        selected = filedialog.askdirectory(
            initialdir=self.dir_var.get(),
            title="Select Download Destination Folder",
        )
        if selected:
            self.dir_var.set(selected)

    def _create_controls(self, parent: ttk.Frame):
        """Action button row: Download, Cancel, Open Folder."""
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(0, 12))

        self.download_btn = ttk.Button(
            btn_frame,
            text="Download Video",
            command=self.start_download,
            style="Primary.TButton",
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0, 8), fill=tk.X, expand=True)

        self.cancel_btn = ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.cancel_download,
            state=tk.DISABLED,
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.open_folder_btn = ttk.Button(
            btn_frame,
            text="Open Folder",
            command=self.open_output_folder,
        )
        self.open_folder_btn.pack(side=tk.LEFT)

    def _create_progress_section(self, parent: ttk.Frame):
        """Progress bar and status text line."""
        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        # Status text (speed, percent, eta)
        self.status_var = tk.StringVar(value="Ready to download.")
        self.status_label = ttk.Label(
            progress_frame,
            textvariable=self.status_var,
            style="Status.TLabel",
        )
        self.status_label.pack(anchor="w", pady=(0, 4))

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient=tk.HORIZONTAL,
            mode="determinate",
            length=100,
        )
        self.progress_bar.pack(fill=tk.X)

    def _create_log_console(self, parent: ttk.Frame):
        """Activity log text console with clear option."""
        log_header = ttk.Frame(parent)
        log_header.pack(fill=tk.X, pady=(4, 2))

        ttk.Label(log_header, text="Activity Log", style="FieldLabel.TLabel").pack(side=tk.LEFT)

        clear_btn = ttk.Button(log_header, text="Clear Log", command=self._clear_logs)
        clear_btn.pack(side=tk.RIGHT)

        # Monospace text view for logs
        log_font = ("Menlo" if is_macos() else "Consolas", 10)
        self.log_text = tk.Text(
            parent,
            height=10,
            font=log_font,
            background=COLORS["log_bg"],
            foreground=COLORS["log_text"],
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=8,
            pady=8,
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.log_text, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text["yscrollcommand"] = scrollbar.set

    def _bind_shortcuts(self):
        """Configures cross-platform keyboard shortcuts for Mac (Cmd) and Windows (Ctrl)."""
        # Ensure Command-key paste/copy works on macOS
        if is_macos():
            for widget in (self.account_entry, self.player_entry, self.video_entry, self.dir_entry):
                widget.bind("<Command-v>", lambda e: e.widget.event_generate("<<Paste>>"))
                widget.bind("<Command-c>", lambda e: e.widget.event_generate("<<Copy>>"))
                widget.bind("<Command-x>", lambda e: e.widget.event_generate("<<Cut>>"))
                widget.bind("<Command-a>", lambda e: self._select_all_entry(e.widget))

        # Enter key triggers download
        self.root.bind("<Return>", lambda e: self.start_download() if not self.is_downloading else None)
        self.root.bind("<Escape>", lambda e: self.cancel_download() if self.is_downloading else None)

    def _select_all_entry(self, widget):
        widget.select_range(0, tk.END)
        return "break"

    def _log(self, text: str):
        """Appends message to log console."""
        self.log_text.insert(tk.END, f"{text}\n")
        self.log_text.see(tk.END)

    def _clear_logs(self):
        """Clears activity log console."""
        self.log_text.delete("1.0", tk.END)

    def start_download(self):
        """Validates inputs and starts background download thread."""
        if self.is_downloading:
            return

        acc = self.account_entry.get()
        pid = self.player_entry.get()
        vid = self.video_entry.get()
        dest_dir = self.dir_var.get()

        try:
            acc, pid, vid = parse_input_fields(acc, pid, vid)
        except ValueError as e:
            messagebox.showwarning("Input Error", str(e), parent=self.root)
            return

        quality_choice = self.quality_var.get()
        q_map = {
            "Best Available": "best",
            "1080p": "1080p",
            "720p": "720p",
            "480p": "480p",
            "Audio Only (M4A/MP3)": "audio",
        }
        quality_key = q_map.get(quality_choice, "best")

        # Set UI state
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_bar["value"] = 0
        self.status_var.set("Connecting to Brightcove...")
        self._log(f"--- Starting Download: Account={acc}, Player={pid}, Video={vid} ---")

        # Instantiate downloader
        self.downloader = BrightcoveDownloader(
            output_dir=dest_dir,
            quality=quality_key,
            progress_cb=lambda p, s, e: self.root.after(0, self._on_progress, p, s, e),
            status_cb=lambda msg: self.root.after(0, self._on_status, msg),
            completion_cb=lambda succ, msg, fp: self.root.after(0, self._on_completion, succ, msg, fp),
        )

        self.download_thread = threading.Thread(
            target=self.downloader.download,
            args=(acc, pid, vid),
            daemon=True,
        )
        self.download_thread.start()

    def cancel_download(self):
        """Requests cancellation from downloader."""
        if self.downloader and self.is_downloading:
            self.cancel_btn.config(state=tk.DISABLED)
            self.status_var.set("Cancelling...")
            self.downloader.cancel()

    def _on_progress(self, percent: float, speed_str: str, eta_str: str):
        """Thread-safe UI update for progress metrics."""
        self.progress_bar["value"] = percent
        self.status_var.set(f"Downloading: {percent:.1f}% | Speed: {speed_str} | ETA: {eta_str}")

    def _on_status(self, message: str):
        """Thread-safe UI update for log messages."""
        self._log(message)

    def _on_completion(self, success: bool, message: str, filepath: Optional[str]):
        """Thread-safe callback upon download termination."""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)

        if success:
            self.progress_bar["value"] = 100
            self.status_var.set("Download Finished Successfully!")
            self.last_downloaded_file = filepath
            messagebox.showinfo(
                "Success",
                f"Video downloaded successfully!\nSaved to: {filepath or self.dir_var.get()}",
                parent=self.root,
            )
        else:
            self.status_var.set(f"Download stopped: {message}")
            if "cancelled" not in message.lower():
                messagebox.showerror("Download Error", f"Failed: {message}", parent=self.root)

    def open_output_folder(self):
        """Opens destination directory in Finder (macOS) or File Explorer (Windows)."""
        target_dir = self.dir_var.get()
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        try:
            if is_macos():
                if self.last_downloaded_file and os.path.exists(self.last_downloaded_file):
                    subprocess.run(["open", "-R", self.last_downloaded_file])
                else:
                    subprocess.run(["open", target_dir])
            elif sys.platform == "win32":
                if self.last_downloaded_file and os.path.exists(self.last_downloaded_file):
                    subprocess.run(["explorer", "/select,", os.path.normpath(self.last_downloaded_file)])
                else:
                    os.startfile(target_dir)
            else:
                subprocess.run(["xdg-open", target_dir])
        except Exception as e:
            self._log(f"Could not open directory: {e}")

    def _on_close(self):
        """Handle window close event."""
        if self.is_downloading and self.downloader:
            if messagebox.askyesno("Exit", "A download is currently in progress. Cancel and exit?", parent=self.root):
                self.downloader.cancel()
                self.root.destroy()
        else:
            self.root.destroy()
