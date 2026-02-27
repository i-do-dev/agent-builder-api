from typing import Annotated
from fastapi import Depends
from api.dependencies.db import Db
from src.adapters.security.password_hasher import PasswordHasher
from src.adapters.security.token_handler import TokenHandler
from src.core.services.password_hasher import IPasswordHasher
from src.core.services.token_handler import ITokenHandler
from src.core.services.user import UserService
from src.handlers.commands.auth.user_signin import UserSignInCommandHandler
from src.handlers.commands.auth.user_signup import UserSignUpCommandHandler
from src.handlers.queries.auth.get_user_profile import GetUserProfileQueryHandler
from settings import Settings

settings = Settings()

def get_user_service(db: Db) -> UserService:
    user_service = UserService(db)
    return user_service

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_token_handler() -> ITokenHandler:
    return TokenHandler(settings)

def get_user_signup_handler(
    user_service: Annotated[UserService, Depends(get_user_service)],
    password_hasher: Annotated[IPasswordHasher, Depends(get_password_hasher)]
) -> UserSignUpCommandHandler:
    return UserSignUpCommandHandler(user_service, password_hasher)

def get_user_signin_handler(
    user_service: Annotated[UserService, Depends(get_user_service)],
    password_hasher: Annotated[IPasswordHasher, Depends(get_password_hasher)],
    token_handler: Annotated[ITokenHandler, Depends(get_token_handler)]
) -> UserSignInCommandHandler:
    return UserSignInCommandHandler(user_service, password_hasher, token_handler)

def get_user_profile_query_handler(
    user_service: Annotated[UserService, Depends(get_user_service)],
    token_handler: Annotated[ITokenHandler, Depends(get_token_handler)]
) -> GetUserProfileQueryHandler:
    return GetUserProfileQueryHandler(user_service, token_handler)

UserSignupCommandHandlerDep = Annotated[UserSignUpCommandHandler, Depends(get_user_signup_handler)]
UserSigninCommandHandlerDep = Annotated[UserSignInCommandHandler, Depends(get_user_signin_handler)]
UserProfileQueryHandlerDep = Annotated[GetUserProfileQueryHandler, Depends(get_user_profile_query_handler)]

UserSignupHandlerDep = UserSignupCommandHandlerDep
UserSigninHandlerDep = UserSigninCommandHandlerDep

