#!/usr/bin/env bash
# ==============================================================================
# Brightcove Video Downloader - macOS Build Script (Randomized Unique Build)
# Generates a uniquely named .app and internal components with a random build ID
# to prevent macOS LaunchServices & Gatekeeper from caching previous versions.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Generate a random 4-digit build number (between 1000 and 9999)
RANDOM_NUM=$((1000 + RANDOM % 9000))
export BUILD_ID="${RANDOM_NUM}"

echo "========================================================"
echo " Packaging Brightcove Video Downloader for macOS"
echo " Unique Build Identifier: ${BUILD_ID}"
echo "========================================================"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 could not be found. Please install Python 3."
    exit 1
fi

# Update core/version.py with unique build info
cat <<EOF > core/version.py
# === CODE INDEX ===
# Version and Build Identifier definitions. Line 6

VERSION = "1.0.0"
BUILD_ID = "${BUILD_ID}"
APP_NAME = "Brightcove Video Downloader ${BUILD_ID}"
EOF

echo "[1/4] Cleaning previous build caches and bytecode..."
rm -rf build dist
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "[2/4] Setting up temporary virtual environment..."
if [ ! -d ".build_venv" ]; then
    python3 -m venv .build_venv
fi
source .build_venv/bin/activate

echo "[3/4] Installing / verifying dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/4] Building standalone macOS Application (.app bundle)..."
pyinstaller --clean -y BrightcoveDownloader.spec

APP_NAME="Brightcove Video Downloader ${BUILD_ID}"
APP_PATH="dist/${APP_NAME}.app"
ZIP_NAME="Brightcove-Downloader-${BUILD_ID}-macOS.zip"

if [ -d "$APP_PATH" ]; then
    # Clear macOS quarantine flag if created locally
    xattr -cr "$APP_PATH" || true

    echo "Compressing into unique distribution ZIP..."
    cd dist
    zip -r -q "${ZIP_NAME}" "${APP_NAME}.app"
    cd ..

    echo "========================================================"
    echo " Build Complete!"
    echo " Application Bundle: dist/${APP_NAME}.app"
    echo " Distributable Zip:  dist/${ZIP_NAME}"
    echo " Internal Executable: dist/${APP_NAME}.app/Contents/MacOS/BrightcoveDownloader_${BUILD_ID}"
    echo "========================================================"
else
    echo "Error: Build failed. Application bundle not found at $APP_PATH"
    exit 1
fi
