from PySide6.QtWidgets import QLabel
from pytestqt.qtbot import QtBot

from scientific_calculator import __version__
from scientific_calculator.ui.main_window import MainWindow


def make_window(qtbot: QtBot) -> MainWindow:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


def test_window_shows_with_title(qtbot: QtBot) -> None:
    window = make_window(qtbot)
    assert window.isVisible()
    assert window.windowTitle() == "Scientific Calculator"


def test_status_bar_shows_version(qtbot: QtBot) -> None:
    window = make_window(qtbot)
    texts = [label.text() for label in window.statusBar().findChildren(QLabel)]
    assert any(__version__ in text for text in texts)


def test_close_hides_window(qtbot: QtBot) -> None:
    window = make_window(qtbot)
    assert window.close()
    assert not window.isVisible()
