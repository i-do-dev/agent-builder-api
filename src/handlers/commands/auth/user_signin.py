from constants import INVALID_CREDENTIALS_ERROR
from src.core.services.password_hasher import IPasswordHasher
from src.core.services.token_handler import ITokenHandler
from src.core.value_objects.password import PlainPassword
from src.handlers.contracts.auth import SignInResult
from src.handlers.errors import AuthenticationError
from src.core.services.user import UserService


class UserSignInCommandHandler:
    def __init__(self, user_service: UserService, password_hasher: IPasswordHasher, token_handler: ITokenHandler) -> None:
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
