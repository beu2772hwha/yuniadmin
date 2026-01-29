from __future__ import annotations

from sqlalchemy import select

from src.db.database import SessionLocal
from src.db.models import Role


class RoleService:
    def list_roles(self) -> list[Role]:
        with SessionLocal() as session:
            roles = session.execute(select(Role).order_by(Role.id)).scalars().all()
            for role in roles:
                session.expunge(role)
            return roles
