from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from api.dependencies.db import Db
from api.services.password_hasher import PasswordHasher
from api.services.token_handler import TokenHandler
from api.services.user_handler import UserHandler
from api.services.user_signin import UserSignIn
from api.services.user_signup import UserSignUp
from api.settings import Settings

settings = Settings()

def get_user_handler(db: Db) -> UserHandler:
    user_service = UserHandler(db)
    return user_service

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_token_handler() -> TokenHandler:
    return TokenHandler(settings)

def get_user_signup_service(
    user_handler: Annotated[UserHandler, Depends(get_user_handler)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)]
) -> UserSignUp:
    return UserSignUp(user_handler, password_hasher)

def get_user_signin_service(
    user_handler: Annotated[UserHandler, Depends(get_user_handler)],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    token_handler: Annotated[TokenHandler, Depends(get_token_handler)]
) -> UserSignIn:
    return UserSignIn(user_handler, password_hasher, token_handler)

UserSignUpSvc = Annotated[UserSignUp, Depends(get_user_signup_service)]
UserSignInSvc = Annotated[UserSignIn, Depends(get_user_signin_service)]

