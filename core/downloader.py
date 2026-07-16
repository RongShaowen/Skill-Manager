"""Skill download from GitHub URLs or direct .zip links.

Security measures:
- HTTPS-only enforcement (delegated to utils.security)
- Download size limit (delegated to utils.security)
- Zip Slip path traversal prevention
- Zip Bomb decompression size limit
- Stream-to-disk download (avoids memory bloat)
- URL validation at entry point
"""

import io
import os
import re
import shutil
import tempfile
import zipfile

import requests

from utils.security import validate_url, MAX_DOWNLOAD_SIZE
from utils.paths import user_skills_dir
from utils.logger import get_logger

_log = get_logger("downloader")

# ── Constants ──────────────────────────────────────────────
MAX_DECOMPRESS_SIZE = 500 * 1024 * 1024  # 500 MB decompression limit
USER_AGENT = "SkillManager/1.4.1"
DOWNLOAD_TIMEOUT = (10, 60)  # (connect_timeout, read_timeout)


# ── Internal helpers ───────────────────────────────────────
def _parse_github_url(url: str) -> tuple[str, str] | None:
    """Extract owner/repo from a GitHub URL. Returns (owner, repo) or None."""
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/.*)?$", url)
    if m:
        return m.group(1), m.group(2)
    return None


def _download_to_file(url: str, headers: dict) -> str:
    """Stream-download *url* into a temp file and return its path.

    Raises on network error, HTTP error, or size exceeded.
    """
    resp = requests.get(url, timeout=DOWNLOAD_TIMEOUT, stream=True, headers=headers)
    resp.raise_for_status()

    fd, tmp_path = tempfile.mkstemp(suffix=".zip")
    try:
        written = 0
        with os.fdopen(fd, "wb") as f:
            for chunk in resp.iter_content(8192):
                written += len(chunk)
                if written > MAX_DOWNLOAD_SIZE:
                    raise ValueError("下载文件过大（超过 50 MB）")
                f.write(chunk)
        return tmp_path
    except Exception:
        os.unlink(tmp_path)
        raise


def _download_github_zip(owner: str, repo: str) -> str:
    """Download a GitHub repo as a zip archive; return temp file path."""
    headers = {"User-Agent": USER_AGENT}
    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
    try:
        return _download_to_file(zip_url, headers)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
            return _download_to_file(zip_url, headers)
        raise


def _download_direct_zip(url: str) -> str:
    """Download a .zip file from a direct URL; return temp file path."""
    headers = {"User-Agent": USER_AGENT}
    return _download_to_file(url, headers)


def _check_zip_bomb(zf: zipfile.ZipFile, max_total: int = MAX_DECOMPRESS_SIZE) -> None:
    """Reject archives whose uncompressed size exceeds *max_total*."""
    total = sum(info.file_size for info in zf.infolist())
    if total > max_total:
        raise ValueError(
            f"压缩包解压后大小（{total / 1024 / 1024:.1f} MB）"
            f"超过安全限制（{max_total / 1024 / 1024:.0f} MB）"
        )


def _safe_extract(zf: zipfile.ZipFile, prefix: str, target_dir: str) -> None:
    """Extract entries under *prefix* to *target_dir*, preventing Zip Slip.

    Any entry whose resolved path escapes *target_dir* is skipped and logged.
    """
    target_dir = os.path.realpath(target_dir)
    for info in zf.infolist():
        name = info.filename
        if not name.startswith(prefix) or (not prefix and "/" in name.rstrip("/")):
            continue
        rel = name[len(prefix):] if prefix else name
        if not rel:
            continue

        out_path = os.path.realpath(os.path.join(target_dir, rel))
        # ── Zip Slip guard ──
        if not out_path.startswith(target_dir + os.sep) and out_path != target_dir:
            _log.warning("Skipping unsafe zip entry (path traversal): %s", name)
            continue

        if name.endswith("/"):
            os.makedirs(out_path, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with zf.open(name) as src, open(out_path, "wb") as dst:
                shutil.copyfileobj(src, dst)


def _find_skill_dir(zf: zipfile.ZipFile) -> str | None:
    """Locate the skill directory inside a zip (the one containing SKILL.md).

    Strategy: collect all directories that contain a SKILL.md, then pick
    the *deepest* one (most specific match).
    """
    skill_dirs: set[str] = set()
    for name in zf.namelist():
        parts = name.split("/")
        for i, part in enumerate(parts):
            if part == "SKILL.md":
                skill_dir = "/".join(parts[:i]) if i > 0 else ""
                skill_dirs.add(skill_dir)

    if not skill_dirs:
        return None
    return max(skill_dirs, key=lambda s: s.count("/"))


# ── Public API ─────────────────────────────────────────────
def download_skill(url: str, progress_callback=None) -> str:
    """Download, validate and install a skill from *url*.

    Parameters
    ----------
    url : str
        HTTPS URL pointing to a GitHub repo or a direct .zip file.
    progress_callback : Callable[[str], None] | None
        Optional callback for status messages.

    Returns
    -------
    str
        The installed skill directory path.

    Raises
    ------
    ValueError
        On validation failure, bad zip, missing SKILL.md, or security issue.
    requests.RequestException
        On network error.
    """
    validate_url(url)

    if progress_callback:
        progress_callback("正在下载...")

    github = _parse_github_url(url)
    if github:
        tmp_path = _download_github_zip(*github)
    else:
        tmp_path = _download_direct_zip(url)

    try:
        if progress_callback:
            progress_callback("正在验证...")

        with zipfile.ZipFile(tmp_path, "r") as zf:
            _check_zip_bomb(zf)
            best = _find_skill_dir(zf)
            if best is None:
                raise ValueError("压缩包中未找到 SKILL.md，不是有效的技能包")

            # Determine skill name and target directory
            target_base = user_skills_dir()
            skill_name = os.path.basename(best.rstrip("/")) or best.split("/")[0]
            target_dir = os.path.join(target_base, skill_name)

            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.makedirs(target_dir, exist_ok=True)

            prefix = best.rstrip("/") + "/" if best else ""
            _safe_extract(zf, prefix, target_dir)
    finally:
        # Always clean up temp file
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    if progress_callback:
        progress_callback("安装完成")

    return target_dir
