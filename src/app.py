from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication

from src.config import get_data_dir
from src.db.init_db import main as init_db
from src.services.settings_service import SettingsService
from src.services.update_service import get_app_root, prepare_update
from src.ui.login_window import LoginWindow
from src.ui.theme import get_stylesheet


def _create_logo() -> Path:
    data_dir = get_data_dir()
    logo_path = data_dir / "yuni_project_logo.png"
    if logo_path.exists():
        return logo_path

    size = 256
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor("#0f172a"))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    base_color = QColor("#2563eb")
    accent = QColor("#22d3ee")
    painter.setBrush(base_color)
    painter.setPen(base_color)
    painter.drawRoundedRect(16, 16, size - 32, size - 32, 48, 48)

    painter.setBrush(accent)
    painter.setPen(accent)
    painter.drawRoundedRect(32, 32, size - 64, size - 64, 36, 36)

    painter.setPen(QColor("#ffffff"))
    font = QFont("Segoe UI", 56, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "YP")

    painter.end()
    pixmap.save(str(logo_path))
    return logo_path


def main() -> None:
    load_dotenv()
    qt_plugins = os.path.join(os.path.dirname(QtCore.__file__), "Qt5", "plugins")
    os.environ.setdefault("QT_PLUGIN_PATH", qt_plugins)
    os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", os.path.join(qt_plugins, "platforms"))

    update_dir = prepare_update()
    if update_dir:
        updater = Path(__file__).resolve().parents[0] / "update_runner.py"
        if updater.exists():
            os.spawnv(
                os.P_NOWAIT,
                sys.executable,
                [sys.executable, str(updater), str(update_dir), str(get_app_root())],
            )
            return

    init_db()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(_create_logo())))
    theme_name = SettingsService().get("theme", "yuni") or "yuni"
    app.setStyleSheet(get_stylesheet(theme_name))
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
