from src.core.entities.user import SecureUser, User
from src.core.services.password_hasher import IPasswordHasher
from src.core.value_objects.password import PlainPassword
from src.handlers.contracts.auth import SignUpCommand, UserProfileResult


class UserServiceMapper:
    @staticmethod
    def signup_command_to_secure_user(command: SignUpCommand, password_hasher: IPasswordHasher) -> SecureUser:
        secure_user = SecureUser(
            username=command.username,
            email=command.email,
            first_name=command.first_name,
            last_name=command.last_name,
        )
        secure_user.set_password(PlainPassword(command.password), password_hasher)
        return secure_user

    @staticmethod
    def entity_to_profile_result(entity: User) -> UserProfileResult:
        return UserProfileResult(
            username=entity.username,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            joined_at=entity.created_at.strftime("%m/%d/%Y %I:%M:%S %p") if entity.created_at else None,
        )
