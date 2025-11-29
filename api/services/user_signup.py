from fastapi import HTTPException, status
from api.constants import FAILED_TO_CREATE_USER_ERROR, PASSWORDS_DO_NOT_MATCH_ERROR
from api.contracts.requests.user import UserSignUpRequest
from api.contracts.responses.user import UserSignUpResponse
from api.dependencies.db import Db
from api.entities.user import AuthUserEntity
from api.mappers.user import UserMapper
from api.services.password_hasher import IPasswordHasher
from api.services.user import UserService
from api.value_objects.password import PlainPassword

class UserSignup:
    def __init__(self, user_handler: UserService, password_hasher: IPasswordHasher) -> None:
        self.user_handler = user_handler
        self.password_hasher = password_hasher
    
    async def signup(self, request: UserSignUpRequest) -> UserSignUpResponse:
        """ Handle user signup logic """
        self._validate_register_request(request)
        
        try:

            user_entity = UserMapper.signup_request_to_entity(request, self.password_hasher)
            print("Mapped User Entity::::::::::::::::::")
            print(user_entity)
            
            # Save user using user service
            #new_user_entity = await self.user_handler.create_user(user_entity)
            new_user_entity = None
            if not new_user_entity:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=FAILED_TO_CREATE_USER_ERROR  
                )
            return UserMapper.entity_to_signup_response(new_user_entity)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
    def _validate_register_request(self, request: UserSignUpRequest) -> None:
        """Validate registration request data."""
        if not self._password_match(request.password, request.confirm_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=PASSWORDS_DO_NOT_MATCH_ERROR
            )

    def _password_match(self, password: str, confirm_password: str) -> bool:
        """Compare password and confirm password."""
        return password == confirm_password
    