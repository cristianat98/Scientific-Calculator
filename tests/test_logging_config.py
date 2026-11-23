import logging
import sys
from collections.abc import Iterator
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest

from scientific_calculator.logging_config import LOG_LEVEL_ENV_VAR, configure_logging


@pytest.fixture(autouse=True)
def restore_root_logger() -> Iterator[None]:
    root = logging.getLogger()
    handlers, level = root.handlers[:], root.level
    yield
    for handler in root.handlers[:]:
        if handler not in handlers:
            root.removeHandler(handler)
            handler.close()
    root.setLevel(level)


def test_default_level_is_info(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(LOG_LEVEL_ENV_VAR, raising=False)
    configure_logging()
    assert logging.getLogger().level == logging.INFO


@pytest.mark.parametrize("value", ["DEBUG", "debug"])
def test_level_from_env(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv(LOG_LEVEL_ENV_VAR, value)
    configure_logging()
    assert logging.getLogger().level == logging.DEBUG


def test_invalid_level_falls_back_to_info(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setenv(LOG_LEVEL_ENV_VAR, "VERBOSE")
    configure_logging()
    assert logging.getLogger().level == logging.INFO
    assert any(r.levelno == logging.WARNING and "VERBOSE" in r.getMessage() for r in caplog.records)


def test_reconfiguring_replaces_previous_handler() -> None:
    configure_logging()
    configure_logging()
    stream_handlers = [h for h in logging.getLogger().handlers if type(h) is logging.StreamHandler]
    assert len(stream_handlers) == 1


@pytest.mark.parametrize(
    ("platform", "env_var", "expected_subdir"),
    [
        ("linux", "XDG_STATE_HOME", Path("scientific-calculator")),
        ("win32", "LOCALAPPDATA", Path("scientific-calculator", "logs")),
        ("darwin", "HOME", Path("Library", "Logs", "scientific-calculator")),
    ],
)
def test_no_stderr_logs_to_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    platform: str,
    env_var: str,
    expected_subdir: Path,
) -> None:
    monkeypatch.setattr(sys, "stderr", None)
    monkeypatch.setattr(sys, "platform", platform)
    monkeypatch.setenv(env_var, str(tmp_path))
    configure_logging()
    logging.getLogger("test").info("hello file")
    file_handlers = [h for h in logging.getLogger().handlers if isinstance(h, RotatingFileHandler)]
    assert len(file_handlers) == 1
    log_file = Path(file_handlers[0].baseFilename)
    assert log_file.parent == tmp_path / expected_subdir
    assert "hello file" in log_file.read_text()
