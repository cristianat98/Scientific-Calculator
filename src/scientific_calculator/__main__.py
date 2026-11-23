"""Application entry point: ``python -m scientific_calculator [--smoke]``."""

import argparse
import logging
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from scientific_calculator import __version__
from scientific_calculator.logging_config import configure_logging
from scientific_calculator.ui.main_window import APP_TITLE, MainWindow

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Start the desktop app and return its exit code.

    With ``--smoke`` the main window is shown and the app quits immediately, as a headless
    launch check for CI and packaged builds.
    """
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(prog="scientific-calculator")
    parser.add_argument("--smoke", action="store_true", help="start, show the window, and quit")
    args, qt_args = parser.parse_known_args(argv)

    configure_logging()
    logger.info("Starting %s v%s", APP_TITLE, __version__)

    app = QApplication.instance() or QApplication([sys.argv[0], *qt_args])
    window = MainWindow()
    window.show()
    if args.smoke:
        logger.info("Smoke mode: quitting after start-up")
        QTimer.singleShot(0, app.quit)

    exit_code = app.exec()
    logger.info("Shutting down with exit code %d", exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
