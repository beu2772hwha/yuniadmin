from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from src.services.auth_service import AuthService
from src.services.logging_service import LoggingService
from src.ui.main_window import MainWindow


class LoginWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(360, 200)

        self._auth = AuthService()
        self._logger = LoggingService()

        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("Логин", self.login_input)
        form.addRow("Пароль", self.password_input)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self._on_login)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.status_label)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def _on_login(self) -> None:
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        admin = self._auth.authenticate(login, password)
        if not admin:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
            return

        self._logger.log(admin.id, f"Вход: {admin.login}")
        self.main_window = MainWindow(admin)
        self.main_window.show()
        self.accept()
