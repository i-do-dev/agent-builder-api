from pwdlib import PasswordHash
from src.core.services.password_hasher import IPasswordHasher


class PasswordHasher(IPasswordHasher):
    def __init__(self):
        self._hasher = PasswordHash.recommended()

    def hash(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._hasher.verify(plain_password, hashed_password)
