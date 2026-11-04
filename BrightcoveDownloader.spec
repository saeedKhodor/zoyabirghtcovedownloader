# -*- mode: python ; coding: utf-8 -*-
# === CODE INDEX ===
# Analysis configuration                   Line 11
# PYZ configuration                        Line 25
# EXE configuration                        Line 28
# COLLECT configuration                    Line 44
# BUNDLE configuration (macOS .app)        Line 54

import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

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
    name='BrightcoveDownloader',
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
    name='BrightcoveDownloader',
)

app = BUNDLE(
    coll,
    name='Brightcove Video Downloader.app',
    icon=None,
    bundle_identifier='com.brightcove.downloader',
    info_plist={
        'CFBundleName': 'Brightcove Video Downloader',
        'CFBundleDisplayName': 'Brightcove Video Downloader',
        'CFBundleIdentifier': 'com.brightcove.downloader',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',
        'LSMinimumSystemVersion': '11.0.0',
    },
)
