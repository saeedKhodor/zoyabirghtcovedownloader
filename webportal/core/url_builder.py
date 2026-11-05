# === CODE INDEX ===
# normalize_player_id(player_id)           Line 14
# build_brightcove_urls(account_id, ...)   Line 28
# parse_input_fields(...)                  Line 50

"""
Brightcove URL construction and normalization utility.
Handles account, player, and video IDs, resolving the proper player URL format.
"""

from typing import List, Tuple
import re


def normalize_player_id(player_id: str) -> str:
    """
    Normalizes the Brightcove player ID.
    Brightcove web embed paths require {player_id}_default or {player_id}_{app_id}.
    If the user entered 'default' or omitted it, defaults to 'default_default'.
    If the user entered 'I5U1azlXZ', appends '_default' if not already present.
    """
    cleaned = (player_id or "").strip()
    if not cleaned or cleaned.lower() == "default":
        return "default_default"
    if not cleaned.endswith("_default") and "_" not in cleaned:
        return f"{cleaned}_default"
    return cleaned


def build_brightcove_urls(account_id: str, player_id: str, video_id: str) -> List[str]:
    """
    Builds primary and fallback URLs for Brightcove player embed.
    Primary: with normalized player ID (e.g. {player_id}_default).
    Fallback: exact player ID as typed (if different) and default_default fallback.
    """
    acc = str(account_id).strip()
    vid = str(video_id).strip()
    raw_pid = str(player_id).strip() if player_id else "default"
    norm_pid = normalize_player_id(raw_pid)

    urls = []
    # Primary URL with normalized player id
    urls.append(f"https://players.brightcove.net/{acc}/{norm_pid}/index.html?videoId={vid}")

    # If raw player id is different from normalized, try raw as fallback
    if raw_pid and raw_pid != norm_pid:
        urls.append(f"https://players.brightcove.net/{acc}/{raw_pid}/index.html?videoId={vid}")

    # Universal default fallback if custom player fails
    fallback_default = f"https://players.brightcove.net/{acc}/default_default/index.html?videoId={vid}"
    if fallback_default not in urls:
        urls.append(fallback_default)

    return urls


def parse_input_fields(account_id: str, player_id: str, video_id: str) -> Tuple[str, str, str]:
    """
    Validates and cleans input fields.
    Raises ValueError with user-friendly message if critical fields are missing.
    """
    acc = (account_id or "").strip()
    pid = (player_id or "").strip()
    vid = (video_id or "").strip()

    # Also handle if user accidentally pasted full URL into any field
    combined = f"{acc} {pid} {vid}"
    url_match = re.search(r"players\.brightcove\.net/(\d+)/([^/]+)/index\.html\?videoId=(\d+)", combined)
    if url_match:
        acc, pid, vid = url_match.groups()

    if not acc:
        raise ValueError("Account ID is required (e.g. 3887645559001).")
    if not vid:
        raise ValueError("Video ID is required (e.g. 5978804382001).")
    if not pid:
        pid = "default"

    return acc, pid, vid
