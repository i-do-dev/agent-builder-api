from api.constants import EMAIL_ALREADY_REGISTERED_ERROR, PASSWORDS_DO_NOT_MATCH_ERROR
from api.schemas.auth import User, UserData, UserSignUpRequest
from api.db.uow import UnitOfWork

class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def exists(self, email: str) -> bool:
        user = await self.uow.users.get_by_email(email)
        return user is not None

    async def sign_up(self, user_request: UserSignUpRequest) -> User:
        user = await self.exists(user_request.email)
        if user:
            raise ValueError(EMAIL_ALREADY_REGISTERED_ERROR)
        elif user_request.password != user_request.confirm_password:
            raise ValueError(PASSWORDS_DO_NOT_MATCH_ERROR)
        # exclude confirm_password before creating user
        user_dict = user_request.model_dump(exclude={"confirm_password"})
        new_user = await self.uow.users.add(user_dict)
        return new_user
