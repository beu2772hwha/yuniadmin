from __future__ import annotations

from sqlalchemy import select

from src.config import get_default_admin_login, get_default_admin_password
from src.db.database import engine, SessionLocal
from src.db.models import Base, Role, Admin, Setting
from src.services.auth_service import hash_password

DEFAULT_ROLES = [
    ("Главный администратор", "manage_servers,manage_users,view_logs,view_data"),
    ("Администратор", "manage_servers,manage_users,view_logs"),
    ("Модератор", "manage_users,view_logs"),
    ("Наблюдатель", "view_logs,view_data"),
]


def seed_roles(session) -> None:
    for name, permissions in DEFAULT_ROLES:
        exists = session.execute(select(Role).where(Role.name == name)).scalar_one_or_none()
        if not exists:
            session.add(Role(name=name, permissions=permissions))


def seed_admin(session) -> None:
    login = get_default_admin_login()
    exists = session.execute(select(Admin).where(Admin.login == login)).scalar_one_or_none()
    if exists:
        return
    role = session.execute(select(Role).where(Role.name == "Главный администратор")).scalar_one()
    session.add(
        Admin(
            login=login,
            password_hash=hash_password(get_default_admin_password()),
            role_id=role.id,
            is_active=True,
        )
    )


def seed_settings(session) -> None:
    exists = session.execute(select(Setting).where(Setting.key == "theme")).scalar_one_or_none()
    if not exists:
        session.add(Setting(key="theme", value="yuni"))


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_roles(session)
        session.flush()
        seed_admin(session)
        seed_settings(session)
        session.commit()
    print("База инициализирована.")


if __name__ == "__main__":
    main()
