# -*- mode: python ; coding: utf-8 -*-
# === CODE INDEX ===
# Environment & path setup                Line 12
# macOS platform patch (inline)           Line 22
# Build ID resolution                     Line 42
# Analysis configuration                  Line 57
# PYZ / EXE configuration                 Line 72
# COLLECT / BUNDLE configuration          Line 91

import os
import sys
import random
import platform
import subprocess

# Ensure spec directory is at the top of sys.path
spec_dir = os.path.abspath(SPECPATH if "SPECPATH" in globals() else os.getcwd())
if spec_dir not in sys.path:
    sys.path.insert(0, spec_dir)

# Apply macOS platform.mac_ver patch inline to ensure no ModuleNotFoundError
if sys.platform == "darwin" or platform.system() == "Darwin":
    _orig_mac_ver = platform.mac_ver

    def _safe_mac_ver(*args, **kwargs):
        res = _orig_mac_ver(*args, **kwargs)
        if res and res[0] and res[0].strip():
            return res
        try:
            out = subprocess.check_output(
                ["sw_vers", "-productVersion"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            if out:
                return (out, res[1] if res else ("", "", ""), res[2] if res else "")
        except Exception:
            pass
        return ("14.0.0", ("x86_64", "", ""), "10.16")

    platform.mac_ver = _safe_mac_ver

# Resolve dynamic build ID
build_id = os.environ.get("BUILD_ID")
if not build_id:
    try:
        from core.version import BUILD_ID as _bid
        if _bid and _bid != "dev":
            build_id = _bid
    except Exception:
        pass
if not build_id:
    build_id = str(random.randint(1000, 9999))

app_display_name = f"Brightcove Video Downloader {build_id}"
app_bundle_name = f"{app_display_name}.app"
exe_name = f"BrightcoveDownloader_{build_id}"
bundle_identifier = f"com.brightcove.downloader.b{build_id}"

block_cipher = None

# Locate runtime hook safely
runtime_hook_path = os.path.join(spec_dir, "core", "mac_patch.py")
runtime_hooks = [runtime_hook_path] if os.path.exists(runtime_hook_path) else []

a = Analysis(
    ['main.py'],
    pathex=[spec_dir],
    binaries=[],
    datas=[],
    hiddenimports=['yt_dlp', 'tkinter', 'core', 'gui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=runtime_hooks,
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=exe_name,
)

app = BUNDLE(
    coll,
    name=app_bundle_name,
    icon=None,
    bundle_identifier=bundle_identifier,
    info_plist={
        'CFBundleName': app_display_name,
        'CFBundleDisplayName': app_display_name,
        'CFBundleIdentifier': bundle_identifier,
        'CFBundleShortVersionString': f'1.0.{build_id}',
        'CFBundleVersion': str(build_id),
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
        'LSMinimumSystemVersion': '11.0.0',
    },
)
