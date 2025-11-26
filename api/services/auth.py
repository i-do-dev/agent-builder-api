from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from api.constants import PASSWORDS_DO_NOT_MATCH_ERROR
from api.contracts.responses.user import UserSignUpResponse
from api.contracts.token import Token
from api.contracts.user import UserAuth, UserProfile
from api.contracts.requests.user import UserSignUpRequest
from api.mappers.user import UserMapper
from api.services.password import PasswordService
from api.services.user import UserService
from api.services.token import TokenService

class AuthService:
    """Service for handling authentication workflows."""
    
    def __init__(self, user_svc: UserService, token_svc: TokenService, password_svc: PasswordService):
        self.user_svc = user_svc
        self.token_svc = token_svc
        self.password_svc = password_svc
        
    async def authenticate_user(self, username_or_email: str, password: str) -> Optional[UserAuth]:
        """Authenticate a user with username and password."""
        user = await self.user_svc.get_user(username_or_email)
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
    
    def _password_match(self, password: str, confirm_password: str) -> bool:
        """Compare password and confirm password."""
        return password == confirm_password
    
    async def register(self, request: UserSignUpRequest) -> UserSignUpResponse:
        """Register a new user."""
        if not self._password_match(request.password, request.confirm_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=PASSWORDS_DO_NOT_MATCH_ERROR
            )

        try:
            hashed_password = self.password_svc.hash_password(request.password)
            user_entity = UserMapper.signup_request_to_entity(request, hashed_password)
            new_user_entity = await self.user_svc.create(user_entity)
            return UserMapper.entity_to_signup_response(new_user_entity)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            ) from e

    async def get_user(self, token: str) -> UserProfile:
        """Get current user from JWT token."""
        username = self.token_svc.verify_token(token)
        user = await self.user_svc.get_by_username(username)
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