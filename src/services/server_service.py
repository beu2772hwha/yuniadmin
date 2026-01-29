from __future__ import annotations

from sqlalchemy import select

from src.db.database import SessionLocal
from src.db.models import Server
from src.services.crypto import CryptoService
from src.services.mysql_service import MySQLService


class ServerService:
    def __init__(self) -> None:
        self._crypto = CryptoService()
        self._mysql = MySQLService()

    def list_servers(self) -> list[Server]:
        with SessionLocal() as session:
            servers = session.execute(select(Server).order_by(Server.id)).scalars().all()
            for server in servers:
                session.expunge(server)
            return servers

    def create_server(
        self,
        name: str,
        host: str,
        port: int,
        db_name: str,
        db_user: str,
        db_password: str,
    ) -> None:
        with SessionLocal() as session:
            server = Server(
                name=name,
                host=host,
                port=port,
                db_name=db_name,
                db_user=db_user,
                encrypted_password=self._crypto.encrypt(db_password),
                status="unknown",
            )
            session.add(server)
            session.commit()

    def update_server(
        self,
        server_id: int,
        name: str,
        host: str,
        port: int,
        db_name: str,
        db_user: str,
        db_password: str,
    ) -> None:
        with SessionLocal() as session:
            server = session.get(Server, server_id)
            if not server:
                return
            server.name = name
            server.host = host
            server.port = port
            server.db_name = db_name
            server.db_user = db_user
            if db_password:
                server.encrypted_password = self._crypto.encrypt(db_password)
            session.commit()

    def delete_server(self, server_id: int) -> None:
        with SessionLocal() as session:
            server = session.get(Server, server_id)
            if not server:
                return
            session.delete(server)
            session.commit()

    def test_connection(self, server_id: int) -> bool:
        with SessionLocal() as session:
            server = session.get(Server, server_id)
            if not server:
                return False
            password = self._crypto.decrypt(server.encrypted_password)
            result = self._mysql.test_connection(
                host=server.host,
                port=server.port,
                user=server.db_user,
                password=password,
                db_name=server.db_name,
            )
            server.status = "online" if result else "offline"
            session.commit()
            return result
