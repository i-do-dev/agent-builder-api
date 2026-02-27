from constants import COULD_NOT_VALIDATE_CREDENTIALS_ERROR
from src.core.services.token_handler import ITokenHandler
from src.handlers.contracts.auth import UserProfileResult
from src.handlers.errors import AuthenticationError
from src.handlers.mappers.user import UserServiceMapper
from src.core.services.user import UserService


class GetUserProfileQueryHandler:
    def __init__(self, user_service: UserService, token_handler: ITokenHandler) -> None:
        self.user_service = user_service
        self.token_handler = token_handler

    async def get_user(self, token: str) -> UserProfileResult:
        try:
            token_payload = self.token_handler.decode(token)
        except Exception as exc:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR) from exc

        user = await self.user_service.get_by_username(token_payload.sub)
        if user is None:
            raise AuthenticationError(COULD_NOT_VALIDATE_CREDENTIALS_ERROR)
        return UserServiceMapper.entity_to_profile_result(user)
