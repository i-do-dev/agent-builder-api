from typing import Optional
from api.constants import EMAIL_ALREADY_REGISTERED_ERROR, USER_ALREADY_REGISTERED_ERROR
#from api.db.models import User
from api.mappers.user import UserMapper
from api.schemas.auth import UserAuth, UserData, UserProfile
from api.entities.user import UserWithPassword, User
from api.dependencies.db import Db

class UserService:
    """Service for handling user operations and authentication."""
    
    def __init__(self, db: Db):
        self.db = db
    
    async def get_user(self, username_or_email: str) -> Optional[UserAuth]:
        """Get a user by username or email."""
        user = await self.db.user.get_valid(username_or_email)
        if user:
            return UserAuth(
                    id=user.id,
                    username=user.username, 
                    email=user.email, 
                    password=user.password,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    created_at=user.created_at.isoformat()
                )
        return None
    
    async def get_by_username(self, username: str) -> Optional[UserAuth]:
        """Get a user by username."""
        user = await self.db.user.get_by_username(username)
        if user:
            return UserAuth(
                    id=user.id,
                    username=user.username, 
                    email=user.email, 
                    password=user.password,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    created_at=user.created_at.isoformat()
                )
        return None
        
    async def _exists(self, username: str, email: str) -> Exception | None:
        if await self.db.user.get_by_username(username):
            return ValueError(USER_ALREADY_REGISTERED_ERROR)
        if await self.db.user.get_by_email(email):
            return ValueError(EMAIL_ALREADY_REGISTERED_ERROR)
        return None
    
    async def create(self, user_entity: UserWithPassword) -> User:
        """Create a new user if username or email does not exist."""
        if exits := await self._exists(user_entity.username, user_entity.email):
            raise exits        
        try:
            new_user = await self.db.user.add(UserMapper.entity_to_model_with_password(user_entity))
            return UserMapper.model_to_entity(new_user)
        except Exception as e:
            raise RuntimeError(f"User creation failed: {str(e)}") from e