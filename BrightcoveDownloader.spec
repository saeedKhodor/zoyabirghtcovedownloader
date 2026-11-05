# -*- mode: python ; coding: utf-8 -*-
# === CODE INDEX ===
# Build ID & dynamic naming               Line 12
# Analysis configuration                   Line 27
# PYZ configuration                        Line 41
# EXE configuration                        Line 44
# COLLECT configuration                    Line 60
# BUNDLE configuration (macOS .app)        Line 70

import os
import sys
import random

# Obtain dynamic build identifier to avoid macOS LaunchServices caching
build_id = os.environ.get("BUILD_ID")
if not build_id:
    try:
        from core.version import BUILD_ID
        build_id = BUILD_ID if BUILD_ID != "dev" else str(random.randint(1000, 9999))
    except Exception:
        build_id = str(random.randint(1000, 9999))

app_display_name = f"Brightcove Video Downloader {build_id}"
app_bundle_name = f"{app_display_name}.app"
exe_name = f"BrightcoveDownloader_{build_id}"
bundle_identifier = f"com.brightcove.downloader.b{build_id}"

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['yt_dlp', 'tkinter', 'core', 'gui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
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
