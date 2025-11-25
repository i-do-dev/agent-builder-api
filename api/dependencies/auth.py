from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from api.dependencies.common import BearerToken, TokenSvc
from api.dependencies.db import Db
from api.services.auth import AuthService
from api.services.user import UserService
from api.services.password import PasswordService
from api.contracts.user import UserProfile
from api.settings import Settings

settings = Settings()

@lru_cache()
def get_password_service() -> PasswordService:
    return PasswordService()

@lru_cache()
def get_user_service(db: Db) -> UserService:
    user_service = UserService(db)
    return user_service

@lru_cache()
def get_auth_service(
    user_svc: Annotated[UserService, Depends(get_user_service)],
    token_svc: TokenSvc,
    password_svc: Annotated[PasswordService, Depends(get_password_service)],
) -> AuthService:
    return AuthService(user_svc, token_svc, password_svc)
async def get_user(
    bearer_token: BearerToken,
    auth_svc: Annotated[AuthService, Depends(get_auth_service)]
) -> UserProfile:
    return await auth_svc.get_user(bearer_token)

AuthSvc = Annotated[AuthService, Depends(get_auth_service)]
AuthUserSvc = Annotated[UserProfile, Depends(get_user)]