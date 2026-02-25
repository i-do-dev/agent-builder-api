from fastapi import HTTPException, status
from constants import INVALID_CREDENTIALS_ERROR, COULD_NOT_VALIDATE_CREDENTIALS_ERROR
from api.contracts.responses.user import UserProfileResponse
from src.core.entities.user import SecureUser
from api.mappers.user import UserMapper
from src.core.services.password_hasher import IPasswordHasher
from src.core.services.token_handler import TokenHandler
from src.core.services.user_handler import UserHandler
from src.core.value_objects.password import PlainPassword
from api.schemas.auth import Token

class UserSignIn:
    def __init__(self, user_handler: UserHandler, password_hasher: IPasswordHasher, token_handler: TokenHandler) -> None:
        self.user_handler = user_handler
        self.password_hasher = password_hasher
        self.token_handler = token_handler

    async def sign_in(self, username: str, password: str) -> Token:
        """ Handle user sign_in logic """
        try:
            secure_user: SecureUser = await self.user_handler.get_secure_user(username)
            if not secure_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=INVALID_CREDENTIALS_ERROR
                )
            
            ok: bool = secure_user.authenticate(PlainPassword(password), self.password_hasher)
            if not ok:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=INVALID_CREDENTIALS_ERROR
                )
            
            # Create JWT token for successful authentication
            access_token = self.token_handler.create_access_token(data={"sub": username})
            
            return Token(access_token=access_token, token_type="bearer")
        except HTTPException:
            # Re-raise HTTPExceptions as they are already properly formatted
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    async def get_user(self, token: str) -> UserProfileResponse:
        """Get current user from JWT token."""
        token_payload = self.token_handler.decode(token)
        user = await self.user_handler.get_by_username(token_payload.sub)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=COULD_NOT_VALIDATE_CREDENTIALS_ERROR,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserMapper.entity_to_profile_response(user)