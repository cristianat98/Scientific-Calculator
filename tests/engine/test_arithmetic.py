import subprocess
import sys

import pytest

from scientific_calculator.engine.arithmetic import add


def test_add_positive_integers() -> None:
    assert add(2, 3) == 5


def test_add_negative_and_positive() -> None:
    assert add(-7, 4) == -3


def test_add_decimals() -> None:
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_engine_import_does_not_load_qt() -> None:
    code = (
        "import sys, scientific_calculator.engine.arithmetic; "
        "sys.exit(any(m.startswith('PySide6') for m in sys.modules))"
    )
    assert subprocess.run([sys.executable, "-c", code], check=False).returncode == 0
