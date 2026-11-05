#!/usr/bin/env bash
# ==============================================================================
# Brightcove Downloader - 1-Click Local Web Launcher for macOS
# Double-click this file to launch the local web app and open Safari automatically.
# ==============================================================================
cd "$(dirname "$0")"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python 3 Required" message "Please install Python 3 to run Brightcove Downloader."'
    exit 1
fi

# Set up or reuse virtual environment (bypasses macOS PEP 668 restrictions)
if [ ! -d ".venv" ]; then
    echo "First-time setup: creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# Check if yt-dlp is installed
if ! python3 -c "import yt_dlp" 2>/dev/null; then
    echo "Installing required dependency (yt-dlp)..."
    pip install yt-dlp
fi

# Clear any cached bytecode
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Launch local server (automatically opens Safari/Chrome)
python3 server.py
