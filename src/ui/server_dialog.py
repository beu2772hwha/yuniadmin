from __future__ import annotations

from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QPushButton,
)

from src.db.models import Server


class ServerDialog(QDialog):
    def __init__(self, server: Server | None = None) -> None:
        super().__init__()
        self.setWindowTitle("Сервер")
        self.setFixedSize(400, 260)

        self.name_input = QLineEdit()
        self.host_input = QLineEdit()
        self.port_input = QSpinBox()
        self.port_input.setMaximum(65535)
        self.port_input.setValue(3306)
        self.db_name_input = QLineEdit()
        self.db_user_input = QLineEdit()
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("Название", self.name_input)
        form.addRow("Хост", self.host_input)
        form.addRow("Порт", self.port_input)
        form.addRow("БД", self.db_name_input)
        form.addRow("Пользователь", self.db_user_input)
        form.addRow("Пароль", self.db_password_input)

        if server:
            self.name_input.setText(server.name)
            self.host_input.setText(server.host)
            self.port_input.setValue(server.port)
            self.db_name_input.setText(server.db_name)
            self.db_user_input.setText(server.db_user)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def get_values(self) -> dict:
        return {
            "name": self.name_input.text().strip(),
            "host": self.host_input.text().strip(),
            "port": int(self.port_input.value()),
            "db_name": self.db_name_input.text().strip(),
            "db_user": self.db_user_input.text().strip(),
            "db_password": self.db_password_input.text().strip(),
        }
