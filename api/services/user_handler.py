from typing import Optional
from api.constants import EMAIL_ALREADY_REGISTERED_ERROR, USER_ALREADY_REGISTERED_ERROR
from api.entities.user import SecureUser, User
from api.dependencies.db import Db

class UserHandler:
    """Service for handling user operations and authentication."""
    
    def __init__(self, db: Db):
        self.db = db
    
    async def get_secure_user(self, username_or_email: str) -> Optional[SecureUser]:
        """Get a user by username or email."""
        user: SecureUser = await self.db.user.get_valid_secure(username_or_email)
        if user:
            return user
        return None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        user: User = await self.db.user.get_by_username(username)
        if not user:
            return None
        return user
    
    async def _exists(self, username: str, email: str) -> Exception | None:
        if await self.db.user.get_by_username(username):
            return ValueError(USER_ALREADY_REGISTERED_ERROR)
        if await self.db.user.get_by_email(email):
            return ValueError(EMAIL_ALREADY_REGISTERED_ERROR)
        return None
    
    async def create(self, secure_user: SecureUser) -> User:
        """Create a new user if username or email does not exist."""
        if exits := await self._exists(secure_user.username, secure_user.email):
            raise exits        
        try:
            return await self.db.user.add(secure_user)
        except Exception as e:
            raise RuntimeError(f"User creation failed: {str(e)}") from e