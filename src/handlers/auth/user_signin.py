from constants import COULD_NOT_VALIDATE_CREDENTIALS_ERROR, INVALID_CREDENTIALS_ERROR
from src.handlers.auth.password_hasher import IPasswordHasher
from src.handlers.auth.token_handler import TokenHandler
from src.core.value_objects.password import PlainPassword
from src.handlers.contracts.auth import SignInResult, UserProfileResult
from src.handlers.errors import AuthenticationError
from src.handlers.mappers.user import UserServiceMapper
from src.core.services.user import UserService


class UserSigninHandler:
    def __init__(self, user_service: UserService, password_hasher: IPasswordHasher, token_handler: TokenHandler) -> None:
        self.user_service = user_service
        self.password_hasher = password_hasher
        self.token_handler = token_handler

    async def sign_in(self, username: str, password: str) -> SignInResult:
        secure_user = await self.user_service.get_secure_user(username)
        if not secure_user:
            raise AuthenticationError(INVALID_CREDENTIALS_ERROR)

        if not secure_user.authenticate(PlainPassword(password), self.password_hasher):
            raise AuthenticationError(INVALID_CREDENTIALS_ERROR)

        access_token = self.token_handler.create_access_token(data={"sub": username})
        return SignInResult(access_token=access_token)

    async def get_user(self, token: str) -> UserProfileResult:
        try:
            token_payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR) from exc

        user = await self.user_service.get_by_username(token_payload.sub)
        if user is None:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR)
        return UserServiceMapper.entity_to_profile_result(user)
