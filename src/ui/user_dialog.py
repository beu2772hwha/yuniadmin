from __future__ import annotations

from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
)

from src.db.models import Admin, Role


class UserDialog(QDialog):
    def __init__(self, roles: list[Role], admin: Admin | None = None) -> None:
        super().__init__()
        self.setWindowTitle("Пользователь")
        self.setFixedSize(380, 240)

        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.role_combo = QComboBox()
        self.is_active_check = QCheckBox("Активен")
        self.is_active_check.setChecked(True)

        self._roles = roles
        for role in roles:
            self.role_combo.addItem(role.name, role.id)

        form = QFormLayout()
        form.addRow("Логин", self.login_input)
        form.addRow("Пароль", self.password_input)
        form.addRow("Роль", self.role_combo)
        form.addRow("", self.is_active_check)

        if admin:
            self.login_input.setText(admin.login)
            self.is_active_check.setChecked(admin.is_active)
            for idx, role in enumerate(roles):
                if role.id == admin.role_id:
                    self.role_combo.setCurrentIndex(idx)
                    break

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def get_values(self) -> dict:
        return {
            "login": self.login_input.text().strip(),
            "password": self.password_input.text().strip(),
            "role_id": int(self.role_combo.currentData()),
            "is_active": self.is_active_check.isChecked(),
        }
