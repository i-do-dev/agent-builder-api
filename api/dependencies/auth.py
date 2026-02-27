from typing import Annotated
from fastapi import Depends
from api.dependencies.db import Db
from src.handlers.auth.password_hasher import PasswordHasher
from src.handlers.auth.token_handler import TokenHandler
from src.core.services.user import UserService
from src.handlers.auth.user_signin import UserSigninHandler
from src.handlers.auth.user_signup import UserSignupHandler
from settings import Settings

settings = Settings()

def get_user_service(db: Db) -> UserService:
    user_service = UserService(db)
    return user_service

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_token_handler() -> TokenHandler:
    return TokenHandler(settings)

def get_user_signup_handler(
    user_service: Annotated[UserService, Depends(get_user_service)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)]
) -> UserSignupHandler:
    return UserSignupHandler(user_service, password_hasher)

def get_user_signin_handler(
    user_service: Annotated[UserService, Depends(get_user_service)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    token_handler: Annotated[TokenHandler, Depends(get_token_handler)]
) -> UserSigninHandler:
    return UserSigninHandler(user_service, password_hasher, token_handler)

UserSignupHandlerDep = Annotated[UserSignupHandler, Depends(get_user_signup_handler)]
UserSigninHandlerDep = Annotated[UserSigninHandler, Depends(get_user_signin_handler)]

