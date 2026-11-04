# === CODE INDEX ===
# YtDlpLogger.__init__                    Line 21
# YtDlpLogger.debug / info / warning      Line 25
# DownloadCancelledException              Line 40
# BrightcoveDownloader.__init__           Line 46
# BrightcoveDownloader.cancel             Line 60
# BrightcoveDownloader._progress_hook     Line 65
# BrightcoveDownloader.download           Line 95

"""
Downloader worker utilizing yt-dlp with thread-safe callbacks,
custom progress parsing, and fallback URL resolution.
"""

import os
import re
import threading
from typing import Callable, Optional, List
import yt_dlp
from core.url_builder import build_brightcove_urls


class YtDlpLogger:
    """Redirects yt-dlp log messages to GUI callback."""
    def __init__(self, log_cb: Optional[Callable[[str], None]]):
        self.log_cb = log_cb

    def debug(self, msg: str):
        # Filter overly verbose internal debug strings if desired
        if msg.startswith("[debug]"):
            return
        if self.log_cb:
            self.log_cb(msg)

    def info(self, msg: str):
        if self.log_cb:
            self.log_cb(msg)

    def warning(self, msg: str):
        if self.log_cb:
            self.log_cb(f"Warning: {msg}")

    def error(self, msg: str):
        if self.log_cb:
            self.log_cb(f"Error: {msg}")


class DownloadCancelledException(Exception):
    """Raised when user cancels active download."""
    pass


class BrightcoveDownloader:
    """Manages video download workflow in a background thread."""

    def __init__(
        self,
        output_dir: str,
        quality: str = "best",
        progress_cb: Optional[Callable[[float, str, str], None]] = None,
        status_cb: Optional[Callable[[str], None]] = None,
        completion_cb: Optional[Callable[[bool, str, Optional[str]], None]] = None,
    ):
        self.output_dir = output_dir or os.path.expanduser("~/Downloads")
        self.quality = quality
        self.progress_cb = progress_cb
        self.status_cb = status_cb
        self.completion_cb = completion_cb
        self._cancel_requested = False
        self._downloaded_file: Optional[str] = None

    def cancel(self):
        """Signals active download to abort."""
        self._cancel_requested = True
        if self.status_cb:
            self.status_cb("Cancellation requested...")

    def _progress_hook(self, d: dict):
        """Called by yt-dlp on download ticks."""
        if self._cancel_requested:
            raise DownloadCancelledException("Download cancelled by user.")

        status = d.get("status")
        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes") or 0
            percent = 0.0
            if total > 0:
                percent = (downloaded / total) * 100.0
            else:
                raw_str = d.get("_percent_str", "0%").strip().replace("%", "")
                try:
                    # Clean ANSI codes if any
                    clean_str = re.sub(r"\x1b\[[0-9;]*m", "", raw_str)
                    percent = float(clean_str)
                except ValueError:
                    percent = 0.0

            speed_str = d.get("_speed_str") or "Calculating..."
            eta_str = d.get("_eta_str") or "--:--"
            # Strip ANSI color codes
            speed_str = re.sub(r"\x1b\[[0-9;]*m", "", speed_str)
            eta_str = re.sub(r"\x1b\[[0-9;]*m", "", eta_str)

            if self.progress_cb:
                self.progress_cb(percent, speed_str.strip(), eta_str.strip())

        elif status == "finished":
            self._downloaded_file = d.get("filename")
            if self.progress_cb:
                self.progress_cb(100.0, "Done", "00:00")
            if self.status_cb:
                self.status_cb("Processing final video output...")

    def _get_format_spec(self) -> str:
        """Translates user-selected quality to yt-dlp format string."""
        q = (self.quality or "best").lower()
        if q == "1080p":
            return "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        elif q == "720p":
            return "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
        elif q == "480p":
            return "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
        elif q == "audio":
            return "bestaudio/best"
        return "bestvideo+bestaudio/best"

    def download(self, account_id: str, player_id: str, video_id: str):
        """Executes download across candidate URLs until success or error."""
        candidate_urls = build_brightcove_urls(account_id, player_id, video_id)
        os.makedirs(self.output_dir, exist_ok=True)

        outtmpl = os.path.join(self.output_dir, "%(title)s [%(id)s].%(ext)s")
        ydl_opts = {
            "format": self._get_format_spec(),
            "outtmpl": outtmpl,
            "progress_hooks": [self._progress_hook],
            "logger": YtDlpLogger(self.status_cb),
            "quiet": False,
            "no_warnings": False,
            "ignoreerrors": False,
        }

        last_error = None
        for idx, url in enumerate(candidate_urls):
            if self._cancel_requested:
                break

            if self.status_cb:
                self.status_cb(f"Attempting source {idx + 1} of {len(candidate_urls)}...")

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ret_code = ydl.download([url])
                    if ret_code == 0:
                        if self.status_cb:
                            self.status_cb("Download completed successfully!")
                        if self.completion_cb:
                            self.completion_cb(True, "Download complete!", self._downloaded_file)
                        return
            except DownloadCancelledException:
                if self.status_cb:
                    self.status_cb("Download was cancelled.")
                if self.completion_cb:
                    self.completion_cb(False, "Cancelled by user.", None)
                return
            except Exception as e:
                last_error = e
                if self.status_cb:
                    self.status_cb(f"Source {idx + 1} failed: {e}")

        # If all candidates failed
        err_msg = str(last_error) if last_error else "Failed to download video from Brightcove."
        if self.status_cb:
            self.status_cb(f"Error: {err_msg}")
        if self.completion_cb:
            self.completion_cb(False, err_msg, None)
