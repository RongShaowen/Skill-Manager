"""Simple logging utility for Skill Manager."""

import os
import logging
from datetime import datetime

LOG_DIR = os.path.join(os.path.expanduser("~"), ".skill_manager", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"skill_manager_{datetime.now():%Y%m%d}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

# ── Log cleanup ───────────────────────────────────────────
_MAX_LOG_DAYS = 30  # keep at most 30 days of logs


def _cleanup_old_logs() -> None:
    """Remove log files older than _MAX_LOG_DAYS."""
    try:
        cutoff = datetime.now().timestamp() - _MAX_LOG_DAYS * 86400
        for fname in os.listdir(LOG_DIR):
            if not fname.startswith("skill_manager_") or not fname.endswith(".log"):
                continue
            fpath = os.path.join(LOG_DIR, fname)
            if os.path.getmtime(fpath) < cutoff:
                os.unlink(fpath)
    except Exception:
        pass  # non-critical


_cleanup_old_logs()


# ── Public API ─────────────────────────────────────────────
def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance."""
    return logging.getLogger(name)
