import logging
import os
import subprocess
import sys
from collections.abc import Iterator

import pytest
from pytestqt.qtbot import QtBot

from scientific_calculator import __version__
from scientific_calculator.__main__ import main


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


def test_smoke_mode_exits_zero_and_logs_version(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    assert main(["--smoke"]) == 0
    assert any(r.levelno == logging.INFO and __version__ in r.getMessage() for r in caplog.records)


def test_module_entry_point_smoke() -> None:
    env = {**os.environ, "QT_QPA_PLATFORM": "offscreen"}
    result = subprocess.run(
        [sys.executable, "-m", "scientific_calculator", "--smoke"],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert __version__ in result.stderr
