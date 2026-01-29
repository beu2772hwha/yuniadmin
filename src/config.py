from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(key, default)


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def get_data_dir() -> Path:
    data_dir = get_project_root() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_db_path() -> Path:
    raw = get_env("APP_DB_PATH", str(get_data_dir() / "app.db"))
    return Path(raw).expanduser().resolve()


def get_sqlite_url() -> str:
    return f"sqlite:///{get_db_path().as_posix()}"


def get_secret_key() -> bytes:
    key = get_env("APP_SECRET_KEY")
    if key:
        return key.encode("utf-8")
    return Fernet.generate_key()


def get_default_admin_login() -> str:
    return get_env("DEFAULT_ADMIN_LOGIN", "admin") or "admin"


def get_default_admin_password() -> str:
    return get_env("DEFAULT_ADMIN_PASSWORD", "admin123") or "admin123"
