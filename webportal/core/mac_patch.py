# === CODE INDEX ===
# apply_macos_compatibility_patch()        Line 13

"""
macOS compatibility patch for Python and yt-dlp.
Resolves `ValueError: invalid literal for int() with base 10: ''` when
platform.mac_ver() returns empty strings on certain macOS installations/versions.
"""

import platform
import subprocess
import sys


def apply_macos_compatibility_patch():
    """
    Ensures platform.mac_ver() always returns a valid, non-empty version string.
    Prevents yt-dlp and PyInstaller from crashing during version_tuple() integer parsing.
    """
    if sys.platform != "darwin" and platform.system() != "Darwin":
        return

    orig_mac_ver = platform.mac_ver

    def safe_mac_ver(*args, **kwargs):
        res = orig_mac_ver(*args, **kwargs)
        # If release version string is non-empty, use it
        if res and res[0] and res[0].strip():
            return res

        # Fallback 1: Query sw_vers directly from macOS
        try:
            ver_str = subprocess.check_output(
                ["sw_vers", "-productVersion"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            if ver_str:
                return (ver_str, res[1] if res else ("", "", ""), res[2] if res else "")
        except Exception:
            pass

        # Fallback 2: Universal safe macOS version tuple (macOS 14.0)
        return ("14.0.0", ("x86_64", "", ""), "10.16")

    platform.mac_ver = safe_mac_ver


# Auto-apply immediately upon module import
apply_macos_compatibility_patch()
