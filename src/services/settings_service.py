from __future__ import annotations

from sqlalchemy import select

from src.db.database import SessionLocal
from src.db.models import Setting


class SettingsService:
    def get(self, key: str, default: str | None = None) -> str | None:
        with SessionLocal() as session:
            setting = session.execute(select(Setting).where(Setting.key == key)).scalar_one_or_none()
            if not setting:
                return default
            return setting.value

    def set(self, key: str, value: str) -> None:
        with SessionLocal() as session:
            setting = session.execute(select(Setting).where(Setting.key == key)).scalar_one_or_none()
            if setting:
                setting.value = value
            else:
                session.add(Setting(key=key, value=value))
            session.commit()
