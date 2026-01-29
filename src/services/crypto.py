from __future__ import annotations

from cryptography.fernet import Fernet

from src.config import get_secret_key


class CryptoService:
    def __init__(self) -> None:
        self._fernet = Fernet(get_secret_key())

    def encrypt(self, value: str) -> str:
        return self._fernet.encrypt(value.encode("utf-8")).decode("utf-8")

    def decrypt(self, token: str) -> str:
        return self._fernet.decrypt(token.encode("utf-8")).decode("utf-8")
