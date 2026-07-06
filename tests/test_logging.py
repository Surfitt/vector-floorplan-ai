"""Unit tests for loguru logging configuration."""

from __future__ import annotations

from pathlib import Path

import pytest
from loguru import logger

from vector_floorplan_ai.logging import (
    LOG_LEVELS,
    reset_logging,
    resolve_log_level,
    setup_logging,
)


@pytest.fixture(autouse=True)
def _clean_logger() -> None:
    reset_logging()
    yield
    reset_logging()


def test_resolve_log_level_accepts_valid_levels() -> None:
    for level in LOG_LEVELS:
        assert resolve_log_level(level) == level


def test_resolve_log_level_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOG_LEVEL", "debug")
    assert resolve_log_level() == "DEBUG"


def test_resolve_log_level_falls_back_on_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOG_LEVEL", "VERBOSE")
    assert resolve_log_level() == "INFO"


def test_setup_logging_writes_to_file(tmp_path: Path) -> None:
    setup_logging(level="DEBUG", log_dir=tmp_path, console=False)
    logger.debug("file sink test")
    logger.complete()

    log_file = tmp_path / "vector-floorplan-ai.log"
    assert log_file.exists()
    assert "file sink test" in log_file.read_text()


def test_setup_logging_respects_trace_level(tmp_path: Path) -> None:
    setup_logging(level="TRACE", log_dir=tmp_path, console=False)
    logger.trace("trace message")
    logger.complete()

    contents = (tmp_path / "vector-floorplan-ai.log").read_text()
    assert "trace message" in contents


def test_setup_logging_is_idempotent(tmp_path: Path) -> None:
    setup_logging(level="INFO", log_dir=tmp_path, console=False)
    setup_logging(level="DEBUG", log_dir=tmp_path, console=False)
    logger.info("only once")
    logger.complete()

    assert (tmp_path / "vector-floorplan-ai.log").read_text().count("only once") == 1


def test_setup_logging_can_disable_file_sink(tmp_path: Path) -> None:
    setup_logging(level="INFO", log_dir=tmp_path, console=False, log_to_file=False)
    logger.info("console only")
    logger.complete()

    assert not (tmp_path / "vector-floorplan-ai.log").exists()


def test_setup_logging_uses_env_vars(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    monkeypatch.setenv("LOG_FILE", "custom.log")

    setup_logging(console=False)
    logger.info("hidden")
    logger.warning("visible")
    logger.complete()

    contents = (tmp_path / "custom.log").read_text()
    assert "hidden" not in contents
    assert "visible" in contents
