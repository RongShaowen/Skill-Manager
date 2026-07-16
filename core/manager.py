"""Skill file operations: delete, open directory, sync."""

import os
import platform
import shutil
import subprocess
from utils.paths import HOME
from utils.logger import get_logger

_log = get_logger("manager")


# ── Delete ─────────────────────────────────────────────────
def delete_skill(skill_path: str) -> bool:
    """Recursively delete a skill directory. Returns True on success."""
    if not os.path.isdir(skill_path):
        return False
    try:
        shutil.rmtree(skill_path)
        return True
    except Exception as e:
        _log.error("Failed to delete %s: %s", skill_path, e)
        return False


# ── Open directory ─────────────────────────────────────────
def open_skill_dir(skill_path: str) -> bool:
    """Open the skill directory in the system file explorer."""
    if not os.path.isdir(skill_path):
        return False
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(skill_path)
        elif system == "Darwin":
            subprocess.Popen(["open", skill_path])
        else:
            subprocess.Popen(["xdg-open", skill_path])
        return True
    except Exception as e:
        _log.error("Failed to open dir %s: %s", skill_path, e)
        return False


# ── Sync targets ───────────────────────────────────────────
SYNC_TARGETS = {
    "claude": os.path.join(HOME, ".claude", "skills"),
    "agent": os.path.join(HOME, ".agents", "skills"),
    "user": os.path.join(HOME, ".mimocode", "skills"),
}


def sync_skill(skill_path: str, target: str) -> str:
    """Copy a skill to another platform directory (atomic).

    Uses a temporary directory so that a failure mid-copy never
    destroys the existing target data.

    Returns
    -------
    str
        The destination path.

    Raises
    ------
    ValueError
        If *target* is not a recognised key.
    OSError
        On file-system errors.
    """
    if target not in SYNC_TARGETS:
        raise ValueError(f"Unknown target: {target}")

    skill_name = os.path.basename(skill_path)
    dest_dir = os.path.join(SYNC_TARGETS[target], skill_name)
    tmp_dir = dest_dir + ".tmp"

    try:
        # Clean up any leftover temp from a previous failed attempt
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        # Copy source → temp
        shutil.copytree(skill_path, tmp_dir)

        # Atomic replace: temp → dest
        if os.path.exists(dest_dir):
            # On Windows, os.replace cannot replace a directory
            _replace_dir(tmp_dir, dest_dir)
        else:
            os.replace(tmp_dir, dest_dir)

        return dest_dir
    except Exception:
        # Best-effort cleanup on failure
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
        raise


def _replace_dir(src: str, dst: str) -> None:
    """Replace directory *dst* with *src* in a cross-platform way."""
    if platform.system() == "Windows":
        # os.replace works for files; for directories, swap names
        backup = dst + ".bak"
        if os.path.exists(backup):
            shutil.rmtree(backup)
        os.replace(dst, backup)
        os.replace(src, dst)
        shutil.rmtree(backup, ignore_errors=True)
    else:
        os.replace(src, dst)


def get_sync_targets(skill_path: str) -> list[str]:
    """Return list of target keys where this skill can be synced."""
    current_source = None
    for key, base in SYNC_TARGETS.items():
        if skill_path.startswith(base):
            current_source = key
            break
    return [k for k in SYNC_TARGETS if k != current_source]
