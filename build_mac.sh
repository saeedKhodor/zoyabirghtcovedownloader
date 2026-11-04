#!/usr/bin/env bash
# ==============================================================================
# Brightcove Video Downloader - macOS Build Script
# Creates a standalone .app bundle and distributable .dmg for macOS
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================"
echo " Packaging Brightcove Video Downloader for macOS"
echo "========================================================"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 could not be found. Please install Python 3 or run via brew/python.org"
    exit 1
fi

echo "[1/4] Setting up temporary virtual environment..."
python3 -m venv .build_venv
source .build_venv/bin/activate

echo "[2/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[3/4] Building standalone macOS Application (.app bundle)..."
rm -rf build dist
pyinstaller --clean -y BrightcoveDownloader.spec

APP_PATH="dist/Brightcove Video Downloader.app"

if [ -d "$APP_PATH" ]; then
    echo "[4/4] Finalizing app bundle..."
    # Clear macOS quarantine flag if created locally
    xattr -cr "$APP_PATH" || true

    echo "Compressing into distribution ZIP..."
    cd dist
    zip -r -q "Brightcove-Video-Downloader-macOS.zip" "Brightcove Video Downloader.app"
    cd ..

    echo "========================================================"
    echo " Build Complete!"
    echo " Application Bundle: $APP_PATH"
    echo " Distributable Zip:  dist/Brightcove-Video-Downloader-macOS.zip"
    echo "========================================================"
else
    echo "Error: Build failed. Application bundle not found."
    exit 1
fi
