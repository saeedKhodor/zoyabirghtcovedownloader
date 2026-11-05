# Brightcove Downloader - Web Portal

A standalone, lightweight local web dashboard for downloading Brightcove videos directly through Safari, Chrome, or Edge.

---

## How to Run on Mac (Double-Click)
1. Double-click **`launch_web_mac.command`**.
2. It sets up an isolated environment, starts the local server, and **automatically opens Safari**.
3. Enter your **Account ID**, **Player ID**, and **Video ID**, and click **Download Video**.
4. The downloaded video will be saved directly into your **`Downloads`** folder.

> [!NOTE]
> If macOS says you do not have permission to run `launch_web_mac.command` the very first time, run this once in Mac Terminal:
> ```bash
> chmod +x launch_web_mac.command
> ```

---

## How to Run on Windows
Double-click **`launch_web_windows.bat`**.

---

## Manual Run (Terminal / Command Line)
```bash
pip install -r requirements.txt
python server.py
```
