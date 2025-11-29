from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from api.dependencies.common import BearerToken, TokenSvc
from api.dependencies.db import Db
from api.entities.user import SecureUser
from api.services.password import PasswordService
from api.services.auth import AuthService
from api.services.password_hasher import PasswordHasher
from api.services.user_handler import UserHandler
from api.contracts.user import UserProfile
from api.services.user_signup import UserSignup
from api.settings import Settings
from api.value_objects.password import HashedPassword

settings = Settings()

def get_user_service(db: Db) -> UserHandler:
    user_service = UserHandler(db)
    return user_service

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_user_signup_service(
    user_handler: Annotated[UserHandler, Depends(get_user_service)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)]
) -> UserSignup:
    return UserSignup(user_handler, password_hasher)

UserSignupSvc = Annotated[UserSignup, Depends(get_user_signup_service)]

# ============================================
def get_password_service() -> PasswordService:
    return PasswordService()

def get_auth_service(
    user_svc: Annotated[UserHandler, Depends(get_user_service)],
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