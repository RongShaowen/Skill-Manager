"""Security helpers: HTTPS validation, path sanitization."""

import os
from urllib.parse import urlparse

ALLOWED_SCHEMES = ("https",)
MAX_DOWNLOAD_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_url(url: str) -> str:
    """Ensure URL uses HTTPS. Returns the validated URL."""
    parsed = urlparse(url.strip())
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"不支持的协议: {parsed.scheme or '(空)'}，仅支持 HTTPS")
    if not parsed.hostname:
        raise ValueError("无效的 URL")
    return url.strip()


def sanitize_path(base: str, user_input: str) -> str:
    """Resolve user_input under base, rejecting path traversal."""
    base = os.path.realpath(base)
    resolved = os.path.realpath(os.path.join(base, user_input))
    if not resolved.startswith(base + os.sep) and resolved != base:
        raise ValueError("路径穿越检测")
    return resolved


def is_safe_filename(name: str) -> bool:
    """Check if a string is safe to use as a directory name."""
    forbidden = set('<>:"/\\|?*\x00')
    return bool(name) and not any(c in forbidden for c in name)
