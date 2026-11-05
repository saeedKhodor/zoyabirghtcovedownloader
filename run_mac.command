#!/usr/bin/env bash
# ==============================================================================
# Double-clickable runner for macOS Finder (PEP 668 Compliant)
# ==============================================================================
cd "$(dirname "$0")"

# Ensure Python 3 exists
if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python 3 Not Found" message "Please install Python 3 from https://www.python.org/downloads/ to run Brightcove Downloader."'
    exit 1
fi

# Set up or reuse dedicated virtual environment (avoids macOS PEP 668 restrictions)
if [ ! -d ".venv" ]; then
    echo "Creating isolated virtual environment..."
    python3 -m venv .venv
fi

# Activate environment
source .venv/bin/activate

# Check if yt-dlp is installed inside virtual environment
if ! python3 -c "import yt_dlp" 2>/dev/null; then
    echo "First-time setup: installing dependencies..."
    pip install -r requirements.txt
fi

# Clear any cached bytecode to ensure latest code changes run
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Launch application
python3 main.py
