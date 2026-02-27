from constants import PASSWORDS_DO_NOT_MATCH_ERROR
from src.core.services.password_hasher import IPasswordHasher
from src.handlers.contracts.auth import SignUpCommand, UserProfileResult
from src.handlers.errors import ValidationError
from src.handlers.mappers.user import UserServiceMapper
from src.core.services.user import UserService


class UserSignUpCommandHandler:
    def __init__(self, user_service: UserService, password_hasher: IPasswordHasher) -> None:
        self.user_service = user_service
        self.password_hasher = password_hasher

    async def signup(self, command: SignUpCommand) -> UserProfileResult:
        self._validate_register_request(command)
        secure_user = UserServiceMapper.signup_command_to_secure_user(command, self.password_hasher)
        new_user = await self.user_service.create(secure_user)
        return UserServiceMapper.entity_to_profile_result(new_user)

    def _validate_register_request(self, command: SignUpCommand) -> None:
        if not self._password_match(command.password, command.confirm_password):
            raise ValidationError(PASSWORDS_DO_NOT_MATCH_ERROR)

    def _password_match(self, password: str, confirm_password: str) -> bool:
        return password == confirm_password
