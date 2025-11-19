from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.dependencies.db import Db, get_db
from api.services.auth import AuthService
from api.services.user import UserService
from api.services.token import TokenService
from api.services.password import PasswordService
from api.schemas.auth import UserProfile
from api.settings import Settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
settings = Settings()

@lru_cache()
def get_password_service() -> PasswordService:
    return PasswordService()

@lru_cache()
def get_user_service(db: Annotated[Db, Depends(get_db)]) -> UserService:
    user_service = UserService(db)
    return user_service

@lru_cache()
def get_token_service() -> TokenService:
    return TokenService(settings)

@lru_cache()
def get_auth_service(
    user_service: Annotated[UserService, Depends(get_user_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
) -> AuthService:
    return AuthService(user_service, token_service, password_service)

async def get_user(
    token: Annotated[str, Depends(oauth_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserProfile:
    return await auth_service.get_user(token)


Auth = Annotated[AuthService, Depends(get_auth_service)]
AuthUser = Annotated[UserProfile, Depends(get_user)]