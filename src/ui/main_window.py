from __future__ import annotations

from PyQt5.QtCore import Qt
import os
import shutil

from PyQt5.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.db.models import Admin
from src.services.auth_service import AuthService
from src.services.logging_service import LoggingService
from src.services.role_service import RoleService
from src.services.server_service import ServerService
from src.services.settings_service import SettingsService
from src.ui.server_dialog import ServerDialog
from src.ui.user_dialog import UserDialog
from src.ui.theme import get_stylesheet
from src.config import get_db_path
from src.db.database import engine


class MainWindow(QMainWindow):
    def __init__(self, admin: Admin) -> None:
        super().__init__()
        self.setWindowTitle("Админ‑панель")
        self.setMinimumSize(900, 600)

        self._admin = admin
        self._server_service = ServerService()
        self._auth_service = AuthService()
        self._role_service = RoleService()
        self._logger = LoggingService()
        self._settings_service = SettingsService()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self._servers_tab = QWidget()
        self._users_tab = QWidget()
        self._roles_tab = QWidget()
        self._logs_tab = QWidget()
        self._settings_tab = QWidget()

        self.tabs.addTab(self._servers_tab, "Серверы")
        self.tabs.addTab(self._users_tab, "Пользователи")
        self.tabs.addTab(self._roles_tab, "Роли")
        self.tabs.addTab(self._logs_tab, "Логи")
        self.tabs.addTab(self._settings_tab, "Настройки")

        self._setup_servers_tab()
        self._setup_users_tab()
        self._setup_roles_tab()
        self._setup_logs_tab()
        self._setup_settings_tab()

        self.refresh_all()

    def refresh_all(self) -> None:
        self._refresh_servers()
        self._refresh_users()
        self._refresh_roles()
        self._refresh_logs()

    def _setup_servers_tab(self) -> None:
        layout = QVBoxLayout()
        self.servers_table = QTableWidget(0, 6)
        self.servers_table.setHorizontalHeaderLabels([
            "ID", "Название", "Хост", "Порт", "БД", "Статус"
        ])
        self.servers_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.servers_table.setAlternatingRowColors(True)
        self.servers_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.servers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.servers_table.horizontalHeader().setMinimumHeight(34)
        self.servers_table.verticalHeader().setVisible(False)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Добавить")
        edit_btn = QPushButton("Изменить")
        del_btn = QPushButton("Удалить")
        test_btn = QPushButton("Проверить")

        add_btn.clicked.connect(self._add_server)
        edit_btn.clicked.connect(self._edit_server)
        del_btn.clicked.connect(self._delete_server)
        test_btn.clicked.connect(self._test_server)

        for btn in (add_btn, edit_btn, del_btn, test_btn):
            btn_layout.addWidget(btn)

        layout.addWidget(self.servers_table)
        layout.addLayout(btn_layout)
        self._servers_tab.setLayout(layout)

    def _setup_users_tab(self) -> None:
        layout = QVBoxLayout()
        self.users_table = QTableWidget(0, 5)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Логин", "Роль", "Активен", "ID роли"
        ])
        self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.users_table.hideColumn(4)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.horizontalHeader().setMinimumHeight(34)
        self.users_table.verticalHeader().setVisible(False)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Добавить")
        edit_btn = QPushButton("Изменить")

        add_btn.clicked.connect(self._add_user)
        edit_btn.clicked.connect(self._edit_user)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)

        layout.addWidget(self.users_table)
        layout.addLayout(btn_layout)
        self._users_tab.setLayout(layout)

    def _setup_roles_tab(self) -> None:
        layout = QVBoxLayout()
        self.roles_table = QTableWidget(0, 3)
        self.roles_table.setHorizontalHeaderLabels(["ID", "Роль", "Права"])
        self.roles_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.roles_table.setAlternatingRowColors(True)
        self.roles_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.roles_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.roles_table.horizontalHeader().setMinimumHeight(34)
        self.roles_table.verticalHeader().setVisible(False)
        layout.addWidget(self.roles_table)
        self._roles_tab.setLayout(layout)

    def _setup_logs_tab(self) -> None:
        layout = QVBoxLayout()
        self.logs_table = QTableWidget(0, 4)
        self.logs_table.setHorizontalHeaderLabels(["ID", "Админ", "Действие", "Дата"])
        self.logs_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.logs_table.setAlternatingRowColors(True)
        self.logs_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.logs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.logs_table.horizontalHeader().setMinimumHeight(34)
        self.logs_table.verticalHeader().setVisible(False)
        layout.addWidget(self.logs_table)
        self._logs_tab.setLayout(layout)

    def _setup_settings_tab(self) -> None:
        layout = QVBoxLayout()

        title = QLabel("Настройки приложения")
        title.setAlignment(Qt.AlignLeft)

        form = QFormLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Тёмная", "dark")
        self.theme_combo.addItem("Светлая", "light")
        self.theme_combo.addItem("Yuni Project", "yuni")
        self.theme_combo.currentIndexChanged.connect(self._on_theme_change)
        form.addRow("Тема", self.theme_combo)

        buttons = QHBoxLayout()
        backup_btn = QPushButton("Сделать бэкап SQLite")
        restore_btn = QPushButton("Восстановить из бэкапа")
        backup_btn.clicked.connect(self._backup_db)
        restore_btn.clicked.connect(self._restore_db)
        buttons.addWidget(backup_btn)
        buttons.addWidget(restore_btn)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(buttons)
        self._settings_tab.setLayout(layout)
        self._load_settings()

    def _load_settings(self) -> None:
        theme = self._settings_service.get("theme", "yuni") or "yuni"
        index = self.theme_combo.findData(theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

    def _on_theme_change(self) -> None:
        theme = self.theme_combo.currentData()
        if not theme:
            return
        self._settings_service.set("theme", theme)
        app = QApplication.instance()
        if app:
            app.setStyleSheet(get_stylesheet(theme))

    def _backup_db(self) -> None:
        db_path = get_db_path()
        default_name = f"app_backup.db"
        target, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить бэкап",
            os.path.join(os.path.dirname(str(db_path)), default_name),
            "SQLite DB (*.db);;Все файлы (*.*)",
        )
        if not target:
            return
        shutil.copy2(str(db_path), target)
        QMessageBox.information(self, "Готово", "Бэкап сохранён")

    def _restore_db(self) -> None:
        source, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать бэкап",
            os.path.dirname(str(get_db_path())),
            "SQLite DB (*.db);;Все файлы (*.*)",
        )
        if not source:
            return
        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            "Приложение перезапишет текущую базу. Продолжить?",
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        engine.dispose()
        shutil.copy2(source, str(get_db_path()))
        QMessageBox.information(self, "Готово", "База восстановлена. Перезапустите приложение.")

    def _refresh_servers(self) -> None:
        servers = self._server_service.list_servers()
        self.servers_table.setRowCount(0)
        for row, server in enumerate(servers):
            self.servers_table.insertRow(row)
            self.servers_table.setItem(row, 0, QTableWidgetItem(str(server.id)))
            self.servers_table.setItem(row, 1, QTableWidgetItem(server.name))
            self.servers_table.setItem(row, 2, QTableWidgetItem(server.host))
            self.servers_table.setItem(row, 3, QTableWidgetItem(str(server.port)))
            self.servers_table.setItem(row, 4, QTableWidgetItem(server.db_name))
            self.servers_table.setItem(row, 5, QTableWidgetItem(server.status))

    def _refresh_users(self) -> None:
        admins = self._auth_service.list_admins()
        roles = {role.id: role.name for role in self._role_service.list_roles()}
        self.users_table.setRowCount(0)
        for row, admin in enumerate(admins):
            self.users_table.insertRow(row)
            self.users_table.setItem(row, 0, QTableWidgetItem(str(admin.id)))
            self.users_table.setItem(row, 1, QTableWidgetItem(admin.login))
            self.users_table.setItem(row, 2, QTableWidgetItem(roles.get(admin.role_id, "")))
            self.users_table.setItem(row, 3, QTableWidgetItem("Да" if admin.is_active else "Нет"))
            self.users_table.setItem(row, 4, QTableWidgetItem(str(admin.role_id)))

    def _refresh_roles(self) -> None:
        roles = self._role_service.list_roles()
        self.roles_table.setRowCount(0)
        for row, role in enumerate(roles):
            self.roles_table.insertRow(row)
            self.roles_table.setItem(row, 0, QTableWidgetItem(str(role.id)))
            self.roles_table.setItem(row, 1, QTableWidgetItem(role.name))
            self.roles_table.setItem(row, 2, QTableWidgetItem(role.permissions))

    def _refresh_logs(self) -> None:
        from sqlalchemy import select
        from src.db.database import SessionLocal
        from src.db.models import Log, Admin

        with SessionLocal() as session:
            logs = session.execute(select(Log).order_by(Log.id.desc())).scalars().all()
            self.logs_table.setRowCount(0)
            for row, log in enumerate(logs):
                admin = session.get(Admin, log.admin_id)
                self.logs_table.insertRow(row)
                self.logs_table.setItem(row, 0, QTableWidgetItem(str(log.id)))
                self.logs_table.setItem(row, 1, QTableWidgetItem(admin.login if admin else ""))
                self.logs_table.setItem(row, 2, QTableWidgetItem(log.action))
                self.logs_table.setItem(row, 3, QTableWidgetItem(str(log.date_time)))

    def _get_selected_server_id(self) -> int | None:
        row = self.servers_table.currentRow()
        if row < 0:
            return None
        item = self.servers_table.item(row, 0)
        return int(item.text()) if item else None

    def _add_server(self) -> None:
        dialog = ServerDialog()
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        data = dialog.get_values()
        if not data["name"] or not data["host"] or not data["db_name"]:
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return
        self._server_service.create_server(**data)
        self._logger.log(self._admin.id, f"Добавлен сервер: {data['name']}")
        self._refresh_servers()

    def _edit_server(self) -> None:
        server_id = self._get_selected_server_id()
        if not server_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сервер")
            return
        servers = self._server_service.list_servers()
        server = next((s for s in servers if s.id == server_id), None)
        if not server:
            return
        dialog = ServerDialog(server)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        data = dialog.get_values()
        if not data["name"] or not data["host"] or not data["db_name"]:
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return
        self._server_service.update_server(server_id, **data)
        self._logger.log(self._admin.id, f"Изменен сервер: {data['name']}")
        self._refresh_servers()

    def _delete_server(self) -> None:
        server_id = self._get_selected_server_id()
        if not server_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сервер")
            return
        self._server_service.delete_server(server_id)
        self._logger.log(self._admin.id, f"Удален сервер ID: {server_id}")
        self._refresh_servers()

    def _test_server(self) -> None:
        server_id = self._get_selected_server_id()
        if not server_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сервер")
            return
        try:
            ok = self._server_service.test_connection(server_id)
        except Exception as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось подключиться: {exc}")
            ok = False
        self._logger.log(self._admin.id, f"Проверка сервера ID: {server_id}")
        self._refresh_servers()
        QMessageBox.information(self, "Результат", "Соединение успешно" if ok else "Ошибка соединения")

    def _get_selected_admin_id(self) -> int | None:
        row = self.users_table.currentRow()
        if row < 0:
            return None
        item = self.users_table.item(row, 0)
        return int(item.text()) if item else None

    def _add_user(self) -> None:
        roles = self._role_service.list_roles()
        dialog = UserDialog(roles)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        data = dialog.get_values()
        if not data["login"] or not data["password"]:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        self._auth_service.create_admin(**data)
        self._logger.log(self._admin.id, f"Добавлен админ: {data['login']}")
        self._refresh_users()

    def _edit_user(self) -> None:
        admin_id = self._get_selected_admin_id()
        if not admin_id:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя")
            return
        admins = self._auth_service.list_admins()
        admin = next((a for a in admins if a.id == admin_id), None)
        if not admin:
            return
        roles = self._role_service.list_roles()
        dialog = UserDialog(roles, admin)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        data = dialog.get_values()
        if not data["login"]:
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            return
        self._auth_service.update_admin(admin_id, **data)
        self._logger.log(self._admin.id, f"Изменен админ: {data['login']}")
        self._refresh_users()
