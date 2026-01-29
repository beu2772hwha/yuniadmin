from __future__ import annotations

import pymysql


class MySQLService:
    def test_connection(self, host: str, port: int, user: str, password: str, db_name: str) -> bool:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            connect_timeout=5,
        )
        connection.close()
        return True
