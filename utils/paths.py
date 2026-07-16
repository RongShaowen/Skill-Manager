"""Path helpers for skill discovery.

Three-layer discovery strategy:
  1. Known-platform presets  — hard-coded paths for major AI tools
  2. Global recursive scan   — find every directory containing SKILL.md
  3. User-defined sources    — read from ~/.skill_manager/config.json
"""

import json
import os
import re
import glob as _glob
from pathlib import Path

from utils.logger import get_logger

_log = get_logger("paths")

HOME = os.path.expanduser("~")

# ── Layer 1: Known-platform preset paths ───────────────────
# Each tuple: (source_name, glob_pattern)
_KNOWN_SOURCE_PATTERNS: list[tuple[str, str]] = [
    # MiMoCode family
    ("builtin",  os.path.join(HOME, ".local", "share", "mimocode", "builtin_skills", "*", "skills", "*")),
    ("compose",  os.path.join(HOME, ".local", "share", "mimocode", "compose", "*", "skills", "*")),
    ("user",     os.path.join(HOME, ".mimocode", "skills", "*")),

    # Claude / Anthropic
    ("claude",   os.path.join(HOME, ".claude", "skills", "*")),

    # Generic agent platform
    ("agent",    os.path.join(HOME, ".agents", "skills", "*")),

    # OpenAI Codex (global skills)
    ("codex",    os.path.join(HOME, ".codex", "skills", "*")),

    # Trae (ByteDance IDE)
    ("trae",     os.path.join(HOME, ".trae", "skills", "*")),

    # Cursor
    ("cursor",   os.path.join(HOME, ".cursor", "skills", "*")),

    # Windsurf (Codeium)
    ("windsurf", os.path.join(HOME, ".windsurf", "skills", "*")),

    # Continue.dev
    ("continue", os.path.join(HOME, ".continue", "skills", "*")),

    # Aider
    ("aider",    os.path.join(HOME, ".aider", "skills", "*")),

    # Generic MCP skill directory
    ("mcp",      os.path.join(HOME, ".mcp", "skills", "*")),

    # GitHub Copilot (speculative)
    ("github_copilot", os.path.join(HOME, ".github", "copilot", "skills", "*")),

    # VS Code / Cline
    ("cline",    os.path.join(HOME, ".cline", "skills", "*")),
]

# ── Layer 2: Global recursive scan config ──────────────────
_DISCOVERY_ENABLED = True
_DISCOVERY_MAX_DEPTH = 4
_DISCOVERY_IGNORE_DIRS = frozenset({
    "node_modules", "__pycache__", ".git", ".venv", "venv",
    "dist", "build", ".idea", ".vscode", "target", "out",
    "site-packages", "egg-info", ".pytest_cache", ".mypy_cache",
    ".next", ".nuxt", ".output", "coverage", ".turbo",
})

# Directories that are known to contain skills (fast-path hints)
_DISCOVERY_HINT_DIRS = frozenset({
    "skills", "skill", "mcp_servers", "prompts",
})


# ── Config helpers ─────────────────────────────────────────
_CONFIG_DIR = os.path.join(HOME, ".skill_manager")
_CONFIG_FILE = os.path.join(_CONFIG_DIR, "config.json")


def _ensure_config_dir() -> None:
    os.makedirs(_CONFIG_DIR, exist_ok=True)


def load_custom_sources() -> list[tuple[str, str]]:
    """Read user-defined skill source directories from config file.

    Config format (JSON):
        {
          "custom_sources": [
            {"name": "my_team", "path": "D:/team-skills"},
            {"name": "company", "path": "/home/user/company-skills"}
          ]
        }
    """
    if not os.path.isfile(_CONFIG_FILE):
        return []
    try:
        with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        sources = cfg.get("custom_sources", [])
        results: list[tuple[str, str]] = []
        for entry in sources:
            name = entry.get("name", "custom")
            path = os.path.expanduser(entry.get("path", ""))
            if os.path.isdir(path):
                results.append((name, os.path.join(path, "*")))
            else:
                _log.warning("Custom source path not found: %s", path)
        return results
    except Exception as e:
        _log.warning("Failed to load custom sources config: %s", e)
        return []


def save_custom_source(name: str, path: str) -> bool:
    """Add a custom source directory to config file."""
    _ensure_config_dir()
    cfg: dict = {}
    if os.path.isfile(_CONFIG_FILE):
        try:
            with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}

    custom = cfg.setdefault("custom_sources", [])
    # Avoid duplicates
    for existing in custom:
        if existing.get("path") == path:
            return False
    custom.append({"name": name, "path": path})

    try:
        with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        _log.error("Failed to save custom source: %s", e)
        return False


def remove_custom_source(path: str) -> bool:
    """Remove a custom source from config file."""
    if not os.path.isfile(_CONFIG_FILE):
        return False
    try:
        with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        custom = cfg.get("custom_sources", [])
        new_custom = [c for c in custom if c.get("path") != path]
        if len(new_custom) == len(custom):
            return False
        cfg["custom_sources"] = new_custom
        with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        _log.error("Failed to remove custom source: %s", e)
        return False


# ── Public API ─────────────────────────────────────────────
def skill_source_dirs() -> list[tuple[str, str]]:
    """Return (source_name, glob_pattern) for each skill source.

    Combines known presets + custom user-defined sources.
    """
    sources = list(_KNOWN_SOURCE_PATTERNS)
    sources.extend(load_custom_sources())
    return sources


def discover_skills_recursive(
    base_dir: str | None = None,
    max_depth: int = _DISCOVERY_MAX_DEPTH,
    ignore_dirs: frozenset[str] = _DISCOVERY_IGNORE_DIRS,
) -> list[tuple[str, str]]:
    """Recursively find directories containing SKILL.md under *base_dir*.

    This is the "catch-all" layer: if a platform stores skills in an
    unexpected location, we still find them as long as they contain a
    SKILL.md file.

    Returns [("discovered", skill_dir_path), ...].
    """
    if not _DISCOVERY_ENABLED:
        return []

    base = Path(base_dir or HOME).expanduser().resolve()
    if not base.is_dir():
        return []

    results: list[tuple[str, str]] = []
    seen: set[str] = set()

    def _scan(path: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = list(path.iterdir())
        except (PermissionError, OSError):
            return

        has_skill_md = False
        subdirs: list[Path] = []

        for entry in entries:
            if entry.is_file() and entry.name == "SKILL.md":
                has_skill_md = True
            elif entry.is_dir():
                if entry.name in ignore_dirs:
                    continue
                subdirs.append(entry)

        if has_skill_md:
            str_path = str(path)
            if str_path not in seen:
                seen.add(str_path)
                results.append(("discovered", str_path))
            # Don't recurse deeper if this dir itself is a skill
            return

        # Hint-based fast path: if directory name suggests skills container,
        # scan one level deeper even if no SKILL.md at this level
        for sub in subdirs:
            _scan(sub, depth + 1)

    _scan(base, 0)
    return results


def _extract_version_from_path(path: str) -> str:
    """Extract version string from a path like .../builtin_skills/0.1.5/skills/xxx.

    Returns "0.0.0" if no version segment found.
    """
    parts = path.replace("\\", "/").split("/")
    for part in parts:
        # Match semantic version patterns like 0.1.5, 1.2, 2.0.1
        if re.match(r"^\d+\.\d+", part):
            return part
    return "0.0.0"


def _version_key(v: str) -> tuple:
    """Convert version string to comparable tuple."""
    try:
        return tuple(int(x) for x in v.split("."))
    except (ValueError, AttributeError):
        return (0,)


def _deduplicate_by_version(
    results: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """When the same skill name appears in multiple version directories,
    keep only the one with the highest version number.

    e.g. builtin_skills/0.1.3/skills/self-extend  →  dropped
         builtin_skills/0.1.5/skills/self-extend  →  kept
    """
    by_name: dict[str, list[tuple[str, str, str]]] = {}
    for source, path in results:
        name = os.path.basename(path)
        ver = _extract_version_from_path(path)
        by_name.setdefault(name, []).append((source, path, ver))

    deduped: list[tuple[str, str]] = []
    for name, entries in by_name.items():
        if len(entries) == 1:
            deduped.append((entries[0][0], entries[0][1]))
        else:
            # Keep the entry with the highest version
            best = max(entries, key=lambda e: _version_key(e[2]))
            deduped.append((best[0], best[1]))
            _log.info(
                "Deduplicated '%s': kept v%s, dropped %d older versions",
                name, best[2], len(entries) - 1,
            )

    # Sort by source then name for stable ordering
    deduped.sort(key=lambda x: (x[0], os.path.basename(x[1])))
    return deduped


def find_skill_dirs() -> list[tuple[str, str]]:
    """Scan all sources and return [(source_name, skill_dir_path), ...].

    Three-layer strategy:
      1. Known-platform presets (glob patterns)
      2. Global recursive discovery (SKILL.md search under ~)
      3. User-defined custom sources

    After collection, deduplicates by skill name — when the same skill
    exists in multiple version directories (e.g. 0.1.3 and 0.1.5),
    only the latest version is kept.
    """
    results: list[tuple[str, str]] = []
    seen_paths: set[str] = set()

    # Layer 1 + 3: presets + custom
    for source, pattern in skill_source_dirs():
        for d in sorted(_glob.glob(pattern)):
            d = os.path.normpath(d)
            skill_md = os.path.join(d, "SKILL.md")
            if os.path.isfile(skill_md) and d not in seen_paths:
                seen_paths.add(d)
                results.append((source, d))

    # Layer 2: recursive discovery (skipping dirs already found)
    discovered = discover_skills_recursive()
    for source, d in discovered:
        d_norm = os.path.normpath(d)
        if d_norm not in seen_paths:
            seen_paths.add(d_norm)
            results.append((source, d_norm))

    # Deduplicate: same skill name in multiple version dirs → keep latest
    results = _deduplicate_by_version(results)

    _log.info("Skill scan complete: %d unique skills found", len(results))
    return results


def user_skills_dir() -> str:
    """Return the directory where user-created skills are stored."""
    d = os.path.join(HOME, ".mimocode", "skills")
    os.makedirs(d, exist_ok=True)
    return d


# ── Size helpers ───────────────────────────────────────────
def skill_dir_size(path: str) -> int:
    """Return total size in bytes of a skill directory."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
