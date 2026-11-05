# === CODE INDEX ===
# Global State Management                 Line 24
# RequestHandler.do_GET                    Line 38
# RequestHandler.do_POST                   Line 54
# RequestHandler._handle_download          Line 72
# RequestHandler._handle_cancel            Line 104
# RequestHandler._handle_open_folder       Line 114
# find_free_port()                         Line 132
# main()                                   Line 144

"""
Lightweight Localhost Web Server for Brightcove Video Downloader.
Zero external server dependencies (uses standard library http.server).
Automatically opens the user's default browser on launch.
"""

import os
import sys
import json
import socket
import threading
import subprocess
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, List

import core.mac_patch  # Ensures macOS platform version parsing never fails
from core.downloader import BrightcoveDownloader
from core.url_builder import parse_input_fields
from web.ui import get_html_page

# Global thread-safe state
STATE_LOCK = threading.Lock()
ACTIVE_DOWNLOADER = None
STATE: Dict[str, Any] = {
    "status": "idle",       # idle, downloading, completed, error, cancelled
    "percent": 0.0,
    "speed": "",
    "eta": "",
    "message": "Ready to download.",
    "filepath": None,
    "logs": ["Brightcove Downloader Web Service initialized."],
}


class BrightcoveRequestHandler(BaseHTTPRequestHandler):
    """Handles REST API and serves Single Page Web UI."""

    def log_message(self, format, *args):
        # Silence verbose request logs to keep terminal output clean
        pass

    def do_GET(self):
        """Routes GET requests."""
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(get_html_page().encode("utf-8"))
        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            with STATE_LOCK:
                resp = json.dumps(STATE)
            self.wfile.write(resp.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Routes POST requests."""
        if self.path == "/api/download":
            self._handle_download()
        elif self.path == "/api/cancel":
            self._handle_cancel()
        elif self.path == "/api/open-folder":
            self._handle_open_folder()
        else:
            self.send_response(404)
            self.end_headers()

    def _handle_download(self):
        """Starts a background download."""
        global ACTIVE_DOWNLOADER
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            req = json.loads(post_data.decode("utf-8"))
            acc, pid, vid = parse_input_fields(
                req.get("account_id"),
                req.get("player_id"),
                req.get("video_id"),
            )
            quality = req.get("quality", "best")
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        with STATE_LOCK:
            STATE["status"] = "downloading"
            STATE["percent"] = 0.0
            STATE["speed"] = "--"
            STATE["eta"] = "--"
            STATE["message"] = f"Connecting to Brightcove for Video {vid}..."
            STATE["logs"].append(f"Starting Download: Account={acc}, Player={pid}, Video={vid}")

        output_dir = os.path.expanduser("~/Downloads")

        def on_prog(pct, spd, eta):
            with STATE_LOCK:
                STATE["percent"] = pct
                STATE["speed"] = spd
                STATE["eta"] = eta
                STATE["message"] = f"Downloading: {pct:.1f}% ({spd})"

        def on_stat(msg):
            with STATE_LOCK:
                STATE["logs"].append(msg)
                if len(STATE["logs"]) > 200:
                    STATE["logs"] = STATE["logs"][-200:]

        def on_comp(success, msg, path):
            with STATE_LOCK:
                STATE["status"] = "completed" if success else "error"
                STATE["message"] = msg
                STATE["filepath"] = path

        ACTIVE_DOWNLOADER = BrightcoveDownloader(
            output_dir=output_dir,
            quality=quality,
            progress_cb=on_prog,
            status_cb=on_stat,
            completion_cb=on_comp,
        )

        t = threading.Thread(
            target=ACTIVE_DOWNLOADER.download,
            args=(acc, pid, vid),
            daemon=True,
        )
        t.start()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "started"}).encode("utf-8"))

    def _handle_cancel(self):
        """Cancels the active download."""
        global ACTIVE_DOWNLOADER
        if ACTIVE_DOWNLOADER:
            ACTIVE_DOWNLOADER.cancel()
        with STATE_LOCK:
            STATE["status"] = "cancelled"
            STATE["message"] = "Download was cancelled."

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "cancelled"}).encode("utf-8"))

    def _handle_open_folder(self):
        """Opens user Downloads folder in Finder or Explorer."""
        dest = os.path.expanduser("~/Downloads")
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", dest])
            elif sys.platform == "win32":
                os.startfile(dest)
            else:
                subprocess.run(["xdg-open", dest])
        except Exception:
            pass

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))


def find_free_port(start_port: int = 8080) -> int:
    """Finds an available local TCP port."""
    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


def main():
    """Initializes and runs the local web server and opens browser."""
    port = find_free_port(8080)
    server_address = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_address, BrightcoveRequestHandler)

    url = f"http://127.0.0.1:{port}"
    print("=" * 60)
    print(" Brightcove Video Downloader - Local Web Dashboard")
    print(f" Web UI Running at: {url}")
    print(" Press Ctrl+C in this terminal window to stop the server.")
    print("=" * 60)

    # Open browser automatically after half a second
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Brightcove Downloader Web Server...")
        httpd.server_close()


if __name__ == "__main__":
    main()
