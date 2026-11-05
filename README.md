# Brightcove Video Downloader (GUI & macOS Package)

A user-friendly, cross-platform graphical application designed for downloading Brightcove videos using **Account ID**, **Player ID**, and **Video ID**.

---

## Features

- **Graphical User Interface (GUI)**: Clean, native macOS/Windows interface with form fields, quality picker, and directory chooser.
- **Smart URL Resolution**: Automatically handles player variations (e.g. `default`, `I5U1azlXZ`, or `I5U1azlXZ_default`) with automatic fallback.
- **Live Progress Tracking**: Real-time progress bar, download speed, ETA, and activity log console.
- **Background Worker**: Thread-safe downloads so the UI remains completely responsive with interactive Cancel support.
- **Multi-Quality Support**: Select between Best Available, 1080p, 720p, 480p, or Audio Only.
- **macOS Native Integration**: High-DPI Retina support, macOS shortcut bindings (`Cmd+C`, `Cmd+V`, `Cmd+A`), and 1-click "Open Folder" in Finder.

---

## Project Structure

```
ZoyaBrightcoveDownloader/
├── core/
│   ├── __init__.py
│   ├── url_builder.py              # ID normalization & Brightcove URL builder
│   └── downloader.py               # Thread-safe yt-dlp download worker & hooks
├── gui/
│   ├── __init__.py
│   ├── theme.py                    # macOS Aqua & cross-platform ttk theme
│   └── main_window.py              # Main GUI window, controls, logs, shortcuts
├── .github/
│   └── workflows/
│       └── build_mac.yml           # Automated macOS .app builder on GitHub Actions
├── main.py                         # Application entry point
├── BrightcoveDownloader.spec        # PyInstaller spec configured for macOS .app
├── build_mac.sh                    # One-command build script for macOS
├── run_mac.command                 # Double-clickable direct runner for macOS Finder
├── requirements.txt                # Python dependencies
└── BrightCoveDownloader.py         # Original reference script
```

---

## Option 1: Local Web Dashboard (Recommended & Most Reliable)

A lightweight localhost web server with **zero compilation and zero GUI issues**:
1. Double-click **`launch_web_mac.command`** on the Mac (or run `python3 server.py`).
2. It immediately launches a local server and **automatically opens Safari/Chrome** to `http://127.0.0.1:8080`.
3. Enter Account ID, Player ID, and Video ID, click **Download Video**, and the video downloads directly into your Mac's **Downloads** folder with live progress tracking!

---

## Option 2: Native Tkinter Desktop GUI
1. Double-click `run_mac.command` in macOS Finder.
2. If prompted, allow terminal execution. It will automatically check dependencies and open the GUI.

### Option 2: Running via Terminal
```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Launch the application
python3 main.py
```

---

## How to Package as a macOS Standalone Application (`.app`)

### Method A: Build Directly on a Mac (Recommended)
Run the automated build script on macOS:
```bash
chmod +x build_mac.sh
./build_mac.sh
```
This generates:
- `dist/Brightcove Video Downloader.app` (Drag directly into `/Applications`)
- `dist/Brightcove-Video-Downloader-macOS.zip` (Distributable archive)

### Method B: Build in the Cloud via GitHub Actions (Zero Mac Required!)
Because macOS binaries cannot be cross-compiled on Windows, a GitHub Actions workflow is included (`.github/workflows/build_mac.yml`):
1. Push this repository to GitHub.
2. Go to the **Actions** tab in your GitHub repository.
3. Select **Build macOS Application** and click **Run workflow** (or simply push to `main`).
4. Once completed, download the ready-to-run `Brightcove-Video-Downloader-macOS.zip` directly from the Actions run artifacts!

---

## Running on Windows (Development & Testing)

```powershell
pip install -r requirements.txt
python main.py
```
