from __future__ import annotations

from datetime import datetime

from src.db.database import SessionLocal
from src.db.models import Log


class LoggingService:
    def log(self, admin_id: int, action: str) -> None:
        with SessionLocal() as session:
            session.add(Log(admin_id=admin_id, action=action, date_time=datetime.utcnow()))
            session.commit()
