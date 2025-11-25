from typing import Optional
from api.constants import EMAIL_ALREADY_REGISTERED_ERROR, USER_ALREADY_REGISTERED_ERROR
from api.db.models import User
from api.schemas.auth import UserAuth, UserData, UserDataWithPassword, UserProfile
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
        
    async def exists(self, username: str, email: str) -> Exception | None:
        if await self.db.user.get_by_username(username):
            return ValueError(USER_ALREADY_REGISTERED_ERROR)
        if await self.db.user.get_by_email(email):
            return ValueError(EMAIL_ALREADY_REGISTERED_ERROR)
        return None
    
    async def create_user(self, user_data: UserDataWithPassword) -> UserProfile:
        """Create a new user if username or email does not exist."""
        if exits := await self.exists(user_data.username, user_data.email):
            raise exits        
        try:
            user_model = User(**user_data.model_dump())
            new_user = await self.db.user.add(user_model)
            return UserProfile(
                id=str(new_user.id),
                username=new_user.username,
                email=new_user.email,
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                created_at=new_user.created_at.isoformat()
            )
        except Exception as e:
            raise RuntimeError(f"User creation failed: {str(e)}") from e