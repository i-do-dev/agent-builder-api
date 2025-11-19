from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from api.constants import PASSWORDS_DO_NOT_MATCH_ERROR
from api.schemas.auth import Token, UserAuth, UserProfile, UserSignUpRequest
from api.services.password import PasswordService
from api.services.user import UserService
from api.services.token import TokenService

class AuthService:
    """Service for handling authentication workflows."""
    
    def __init__(self, user_svc: UserService, token_svc: TokenService, password_svc: PasswordService):
        self.user_svc = user_svc
        self.token_svc = token_svc
        self.password_svc = password_svc
        
    async def authenticate_user(self, username: str, password: str) -> Optional[UserAuth]:
        """Authenticate a user with username and password."""
        user = await self.user_svc.get_user(username)
        if not user:
            return None
        if not self.password_svc.verify_password(password, user.password):
            return None
        return user
    
    async def login(self, username: str, password: str) -> Token:
        """Authenticate user and return access token."""
        user = await self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=self.token_svc.access_token_expire_minutes)
        access_token = self.token_svc.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    
    def compare_passwords(self, password: str, confirm_password: str) -> bool:
        """Compare password and confirm password."""
        return password == confirm_password
    
    async def register(self, form_data: UserSignUpRequest) -> UserProfile:
        """Register a new user."""
        if not self.compare_passwords(form_data.password, form_data.confirm_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=PASSWORDS_DO_NOT_MATCH_ERROR
            )

        try:
            user_dict = form_data.model_dump(exclude={"password","confirm_password"})
            user_dict["password"] = self.password_svc.get_password_hash(form_data.password)
            user = await self.user_svc.create_user(user_dict)
            return user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            ) from e

    async def get_user(self, token: str) -> UserProfile:
        """Get current user from JWT token."""
        username = self.token_svc.verify_token(token)
        user = await self.user_svc.get_user(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserProfile(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )