#!/usr/bin/env bash
# ==============================================================================
# Double-clickable runner for macOS Finder
# ==============================================================================
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python 3 Not Found" message "Please install Python 3 from https://www.python.org/downloads/ to run Brightcove Downloader."'
    exit 1
fi

# Ensure yt-dlp is available in user environment
python3 -c "import yt_dlp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "First-time setup: installing yt-dlp..."
    python3 -m pip install --user -r requirements.txt
fi

python3 main.py
