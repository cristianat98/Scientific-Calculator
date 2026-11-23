"""Main application window."""

import logging

from PySide6.QtWidgets import QLabel, QMainWindow

from scientific_calculator import __version__

APP_TITLE = "Scientific Calculator"

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Top-level window; shows the app version in the status bar."""

    def __init__(self) -> None:
        """Build the window and its status bar."""
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(480, 640)
        self.statusBar().addPermanentWidget(QLabel(f"v{__version__}"))
        logger.debug("Main window created")
