from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.contracts.responses.user import UserProfileResponse, UserSignUpResponse
from api.dependencies.auth import UserSigninCommandHandlerDep, UserSignupCommandHandlerDep, UserProfileQueryHandlerDep
from api.dependencies.common import BearerToken
from api.contracts.token import Token
from api.contracts.requests.user import UserSignUpRequest
from src.handlers.errors import AuthenticationError, ConflictError, ValidationError
from src.handlers.mappers.auth import AuthApiMapper

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/token", response_model=Token)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    signin_handler: UserSigninCommandHandlerDep
) -> Token:
    try:
        result = await signin_handler.sign_in(form_data.username, form_data.password)
        return AuthApiMapper.signin_result_to_token(result)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

@router.get("/me", response_model=UserProfileResponse)
async def me(
    bearer_token: BearerToken, 
    user_profile_query_handler: UserProfileQueryHandlerDep
    ) -> UserProfileResponse:
    try:
        result = await user_profile_query_handler.get_user(bearer_token)
        return AuthApiMapper.profile_result_to_profile_response(result)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

@router.post("/register", response_model=UserSignUpResponse)
async def register(
    request: Annotated[UserSignUpRequest, Form()],
    user_signup_handler: UserSignupCommandHandlerDep
) -> UserSignUpResponse:
    command = AuthApiMapper.signup_request_to_command(request)
    try:
        result = await user_signup_handler.signup(command)
        return AuthApiMapper.profile_result_to_signup_response(result)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc