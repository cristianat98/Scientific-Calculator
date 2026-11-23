"""Application-wide logging configuration."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_LEVEL_ENV_VAR = "SCIENTIFIC_CALCULATOR_LOG_LEVEL"
APP_DIR_NAME = "scientific-calculator"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

logger = logging.getLogger(__name__)
_handler: logging.Handler | None = None


def _log_dir() -> Path:
    """Return the per-user log directory for the current platform."""
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / APP_DIR_NAME / "logs"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Logs" / APP_DIR_NAME
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / APP_DIR_NAME


def _build_handler() -> logging.Handler:
    """Return a stderr handler, or a rotating file handler when there is no stderr."""
    if sys.stderr is not None:
        return logging.StreamHandler(sys.stderr)
    log_dir = _log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    return RotatingFileHandler(
        log_dir / "app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )


def configure_logging() -> None:
    """Configure the root logger from ``SCIENTIFIC_CALCULATOR_LOG_LEVEL`` (default ``INFO``).

    Calling it again replaces the handler installed by the previous call.
    """
    global _handler
    raw_level = os.environ.get(LOG_LEVEL_ENV_VAR, "INFO")
    level = logging.getLevelNamesMapping().get(raw_level.strip().upper())

    root = logging.getLogger()
    if _handler is not None:
        root.removeHandler(_handler)
        _handler.close()
    _handler = _build_handler()
    _handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root.addHandler(_handler)
    root.setLevel(level if level is not None else logging.INFO)

    if level is None:
        logger.warning("Invalid %s value %r; using INFO", LOG_LEVEL_ENV_VAR, raw_level)
    logger.debug("Logging configured with handler %s", type(_handler).__name__)
