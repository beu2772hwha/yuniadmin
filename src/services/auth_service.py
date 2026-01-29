from __future__ import annotations

from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import select

from src.db.database import SessionLocal
from src.db.models import Admin, Role

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


class AuthService:
    def authenticate(self, login: str, password: str) -> Optional[Admin]:
        with SessionLocal() as session:
            admin = session.execute(select(Admin).where(Admin.login == login)).scalar_one_or_none()
            if not admin or not admin.is_active:
                return None
            if not verify_password(password, admin.password_hash):
                return None
            session.expunge(admin)
            return admin

    def create_admin(self, login: str, password: str, role_id: int, is_active: bool = True) -> Admin:
        with SessionLocal() as session:
            admin = Admin(
                login=login,
                password_hash=hash_password(password),
                role_id=role_id,
                is_active=is_active,
            )
            session.add(admin)
            session.commit()
            session.refresh(admin)
            session.expunge(admin)
            return admin

    def update_admin(self, admin_id: int, login: str, password: Optional[str], role_id: int, is_active: bool) -> None:
        with SessionLocal() as session:
            admin = session.get(Admin, admin_id)
            if not admin:
                return
            admin.login = login
            if password:
                admin.password_hash = hash_password(password)
            admin.role_id = role_id
            admin.is_active = is_active
            session.commit()

    def list_admins(self) -> list[Admin]:
        with SessionLocal() as session:
            admins = session.execute(select(Admin).order_by(Admin.id)).scalars().all()
            for admin in admins:
                session.expunge(admin)
            return admins

    def get_roles(self) -> list[Role]:
        with SessionLocal() as session:
            roles = session.execute(select(Role).order_by(Role.id)).scalars().all()
            for role in roles:
                session.expunge(role)
            return roles
