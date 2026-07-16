"""Skill marketplace — browse and install community skills.

Network strategy (tried in order):
  1. GitHub raw (official)
  2. ghfast.top mirror (China-friendly)
  3. Local cache (offline fallback)
  4. Built-in bundled list (always available)

Each remote source is retried twice with exponential back-off.
Successful responses are cached to disk for offline use.

Error reporting: returns a list of error strings so the UI can show
the user exactly which sources were tried and why they failed.
"""

import json
import os
import time

import requests

from utils.logger import get_logger

_log = get_logger("marketplace")

# ── Constants ──────────────────────────────────────────────
USER_AGENT = "SkillManager/1.4.0"
REQUEST_TIMEOUT = (5, 15)  # (connect, read)
MAX_RETRIES = 2
BACKOFF_BASE = 1.5  # seconds

_GITHUB_RAW_TEMPLATE = (
    "https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file}"
)
_MIRROR_TEMPLATE = "https://ghfast.top/https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file}"

# Multiple marketplace sources — tried in order until one works
_DEFAULT_SOURCES: list[dict] = [
    {
        "owner": "AstraBert",
        "repo": "micode-skills",
        "branch": "main",
        "file": "marketplace.json",
    },
    {
        "owner": "AstraBert",
        "repo": "micode-skills",
        "branch": "master",
        "file": "marketplace.json",
    },
]

# ── Built-in marketplace fallback ──────────────────────────
# Always available even with no network. Contains well-known
# skill repos that users can install.
_BUILTIN_MARKETPLACE: list[dict] = [
    {
        "name": "claude-code-skills",
        "description": "Anthropic 官方 Claude Code 技能合集（PDF、DOCX、PPTX、XLSX 等）",
        "url": "https://github.com/anthropics/claude-code",
        "category": "官方技能",
        "author": "Anthropic",
    },
    {
        "name": "mimocode-skills",
        "description": "MiMoCode 官方技能合集（深度研究、学术论文、飞书集成等）",
        "url": "https://github.com/AstraBert/micode",
        "category": "官方技能",
        "author": "MiMoCode",
    },
    {
        "name": "awesome-claude-skills",
        "description": "社区维护的 Claude 技能精选列表",
        "url": "https://github.com/hesreallyhim/awesome-claude-code",
        "category": "社区精选",
        "author": "Community",
    },
]

# ── Cache ──────────────────────────────────────────────────
_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".skill_manager", "cache")
_CACHE_FILE = os.path.join(_CACHE_DIR, "marketplace.json")
_CACHE_META = os.path.join(_CACHE_DIR, "marketplace_meta.json")


def _ensure_cache_dir() -> None:
    os.makedirs(_CACHE_DIR, exist_ok=True)


def _save_cache(data: list[dict]) -> None:
    _ensure_cache_dir()
    try:
        with open(_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        meta = {"updated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        with open(_CACHE_META, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    except Exception as e:
        _log.warning("Failed to save marketplace cache: %s", e)


def _load_cache() -> list[dict] | None:
    if not os.path.isfile(_CACHE_FILE):
        return None
    try:
        with open(_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception as e:
        _log.warning("Failed to load marketplace cache: %s", e)
    return None


def _cache_timestamp() -> str | None:
    if not os.path.isfile(_CACHE_META):
        return None
    try:
        with open(_CACHE_META, "r", encoding="utf-8") as f:
            meta = json.load(f)
        return meta.get("updated_at")
    except Exception:
        return None


# ── Validation ────────────────────────────────────────────
_REQUIRED_FIELDS = {"name", "url"}


def _validate_entries(data: list[dict]) -> list[dict]:
    """Strip out entries missing required fields or with invalid URLs."""
    valid = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        if not _REQUIRED_FIELDS.issubset(entry.keys()):
            _log.warning("Skipping marketplace entry missing fields: %s", entry)
            continue
        name = entry.get("name", "")
        url = entry.get("url", "")
        if not name or not url:
            continue
        if not url.startswith("https://"):
            _log.warning("Skipping entry with non-HTTPS url: %s", url)
            continue
        valid.append(entry)
    return valid


# ── Network fetch ──────────────────────────────────────────
def _build_url(template: str, source: dict) -> str:
    return template.format(**source)


def _fetch_from_url(url: str) -> tuple[list[dict] | None, str | None]:
    """Try to fetch JSON from *url*.

    Returns (data, error_message). On success error_message is None.
    """
    try:
        resp = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data, None
        if isinstance(data, dict) and "skills" in data:
            return data["skills"], None
        return None, f"返回数据格式异常（HTTP {resp.status_code}）"
    except requests.exceptions.Timeout:
        return None, "连接超时（GitHub 可能被墙）"
    except requests.exceptions.ConnectionError as e:
        return None, f"网络连接失败：{e}"
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response is not None else "?"
        return None, f"HTTP {code} 错误"
    except Exception as e:
        return None, f"未知错误：{e}"


def _fetch_with_retry(url: str, retries: int = MAX_RETRIES) -> tuple[list[dict] | None, str | None]:
    """Fetch with exponential back-off retry."""
    last_error: str | None = None
    for attempt in range(retries + 1):
        result, err = _fetch_from_url(url)
        if result is not None:
            return result, None
        last_error = err
        if attempt < retries:
            wait = BACKOFF_BASE ** attempt
            _log.debug("Retrying in %.1fs (attempt %d/%d)", wait, attempt + 1, retries)
            time.sleep(wait)
    return None, last_error


# ── Public API ─────────────────────────────────────────────
def fetch_marketplace(
    sources: list[dict] | None = None,
) -> tuple[list[dict], str | None, bool, list[str]]:
    """Fetch the community skill marketplace index.

    Parameters
    ----------
    sources : list[dict] | None
        Override the default remote sources.
        Each dict has keys: owner, repo, branch, file.

    Returns
    -------
    tuple[list[dict], str | None, bool, list[str]]
        - skill_list: validated list of marketplace entries.
        - cache_timestamp: when cache was last updated (if used).
        - used_cache: True if result came from local cache.
        - errors: list of error strings for each failed source
          (empty on success). UI can display these to the user.
    """
    src_list = sources or _DEFAULT_SOURCES
    errors: list[str] = []

    for src in src_list:
        # 1) Try GitHub raw (official)
        github_url = _build_url(_GITHUB_RAW_TEMPLATE, src)
        data, err = _fetch_with_retry(github_url)
        if data is not None:
            validated = _validate_entries(data)
            _save_cache(validated)
            _log.info("Marketplace loaded from GitHub: %d entries", len(validated))
            return validated, None, False, []

        errors.append(f"GitHub 原站 ({src['owner']}/{src['repo']}): {err}")

        # 2) Try China-friendly mirror
        mirror_url = _build_url(_MIRROR_TEMPLATE, src)
        data, err2 = _fetch_with_retry(mirror_url)
        if data is not None:
            validated = _validate_entries(data)
            _save_cache(validated)
            _log.info("Marketplace loaded from mirror: %d entries", len(validated))
            return validated, None, False, []

        errors.append(f"国内镜像 (ghfast.top): {err2}")

    # 3) Fallback to local cache
    _log.warning("All remote sources failed, trying local cache")
    cached = _load_cache()
    if cached is not None:
        ts = _cache_timestamp()
        errors.append(f"已使用本地缓存（更新于 {ts}）")
        return _validate_entries(cached), ts, True, errors

    # 4) Built-in fallback list (always available)
    _log.warning("No cache available, using built-in marketplace list")
    errors.append("使用内置技能列表（网络不可用）")
    return _BUILTIN_MARKETPLACE, None, False, errors


def is_installed(skill_name: str, installed_names: set[str]) -> bool:
    """Check if a marketplace skill is already installed."""
    return skill_name in installed_names
