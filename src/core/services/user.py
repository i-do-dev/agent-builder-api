from typing import Optional

from constants import EMAIL_ALREADY_REGISTERED_ERROR, USER_ALREADY_REGISTERED_ERROR
from src.adapters.db.uow import UnitOfWork
from src.core.entities.user import SecureUser, User
from src.handlers.errors import ConflictError


class UserService:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def get_secure_user(self, username_or_email: str) -> Optional[SecureUser]:
        return await self.db.user.get_valid_secure(username_or_email)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.db.user.get_by_username(username)

    async def _exists(self, username: str, email: str) -> Exception | None:
        if await self.db.user.get_by_username(username):
            return ConflictError(USER_ALREADY_REGISTERED_ERROR)
        if await self.db.user.get_by_email(email):
            return ConflictError(EMAIL_ALREADY_REGISTERED_ERROR)
        return None

    async def create(self, secure_user: SecureUser) -> User:
        if exists_error := await self._exists(secure_user.username, secure_user.email):
            raise exists_error
        return await self.db.user.add(secure_user)
