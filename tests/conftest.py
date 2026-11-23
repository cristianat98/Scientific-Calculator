import logging
import os
from collections.abc import Iterator
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# Subprocess tests run `python -m scientific_calculator` without the package being installed.
_SRC = str(Path(__file__).resolve().parents[1] / "src")
os.environ["PYTHONPATH"] = os.pathsep.join(filter(None, [_SRC, os.environ.get("PYTHONPATH")]))


@pytest.fixture(autouse=True)
def restore_root_logger() -> Iterator[None]:
    """Undo root-logger changes made by configure_logging() during a test."""
    root = logging.getLogger()
    handlers, level = root.handlers[:], root.level
    yield
    for handler in root.handlers[:]:
        if handler not in handlers:
            root.removeHandler(handler)
            handler.close()
    root.setLevel(level)
