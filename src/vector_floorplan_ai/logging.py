"""Loguru-based logging for scripts and library code.

Call ``setup_logging()`` once at the start of every script or CLI entry point::

    from vector_floorplan_ai.logging import logger, setup_logging

    setup_logging()
    logger.info("Starting pipeline")
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Final

from loguru import logger

__all__ = ["LOG_LEVELS", "logger", "reset_logging", "resolve_log_level", "setup_logging"]

LOG_LEVELS: Final[tuple[str, ...]] = (
    "TRACE",
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
)

_DEFAULT_LEVEL: Final[str] = "INFO"
_DEFAULT_LOG_DIR: Final[str] = "logs"
_DEFAULT_LOG_FILE: Final[str] = "vector-floorplan-ai.log"

_FILE_FORMAT: Final[str] = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}"
)
_CONSOLE_FORMAT: Final[str] = (
    "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)

_configured = False


def resolve_log_level(level: str | None = None) -> str:
    """Return a valid loguru level name (defaults to env LOG_LEVEL or INFO)."""
    raw = (level or os.getenv("LOG_LEVEL", _DEFAULT_LEVEL)).strip().upper()
    if raw in LOG_LEVELS:
        return raw
    logger.warning("Invalid LOG_LEVEL {!r}; falling back to INFO", raw)
    return _DEFAULT_LEVEL


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def reset_logging() -> None:
    """Remove all handlers. Used by tests and for reconfiguration."""
    global _configured
    logger.remove()
    _configured = False


def setup_logging(
    *,
    level: str | None = None,
    log_dir: Path | str | None = None,
    log_file: str | None = None,
    console: bool | None = None,
    log_to_file: bool | None = None,
) -> None:
    """Configure loguru for console and rotating file output.

    Settings can be overridden via environment variables:

    - ``LOG_LEVEL`` — TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    - ``LOG_DIR`` — directory for log files (default: ``logs``)
    - ``LOG_FILE`` — log file name (default: ``vector-floorplan-ai.log``)
    - ``LOG_TO_CONSOLE`` — enable stderr sink (default: true)
    - ``LOG_TO_FILE`` — enable file sink (default: true)
    """
    global _configured
    if _configured:
        return

    resolved_level = resolve_log_level(level)
    resolved_log_dir = Path(log_dir or os.getenv("LOG_DIR", _DEFAULT_LOG_DIR))
    resolved_log_file = log_file or os.getenv("LOG_FILE", _DEFAULT_LOG_FILE)
    enable_console = console if console is not None else _env_flag("LOG_TO_CONSOLE", True)
    enable_file = log_to_file if log_to_file is not None else _env_flag("LOG_TO_FILE", True)

    logger.remove()

    if enable_console:
        logger.add(
            sys.stderr,
            level=resolved_level,
            format=_CONSOLE_FORMAT,
            colorize=True,
            backtrace=True,
            diagnose=False,
        )

    if enable_file:
        resolved_log_dir.mkdir(parents=True, exist_ok=True)
        log_path = resolved_log_dir / resolved_log_file
        logger.add(
            log_path,
            level=resolved_level,
            format=_FILE_FORMAT,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            enqueue=True,
            backtrace=True,
            diagnose=False,
        )
        logger.debug("File logging enabled at {}", log_path.resolve())

    _configured = True
    logger.log(resolved_level, "Logging initialized (level={})", resolved_level)
