from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from api.contracts.responses.user import UserProfileResponse, UserSignUpResponse
from api.dependencies.auth import UserSignInSvc, UserSignUpSvc, get_user_signin_service
from api.dependencies.common import BearerToken
from api.contracts.token import Token
from api.contracts.requests.user import UserSignUpRequest
from api.services.user_signin import UserSignIn

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/token", response_model=Token)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    signin_svc: UserSignInSvc
) -> Token:
    return await signin_svc.sign_in(form_data.username, form_data.password)

@router.get("/me", response_model=UserProfileResponse)
async def me(
    bearer_token: BearerToken, 
    user_signin_svc: Annotated[UserSignIn, Depends(get_user_signin_service)]
    ) -> UserProfileResponse:
    return await user_signin_svc.get_user(bearer_token)

@router.post("/register", response_model=UserSignUpResponse)
async def register(
    request: Annotated[UserSignUpRequest, Form()],
    user_signup_svc: UserSignUpSvc
) -> UserSignUpResponse:
    return await user_signup_svc.signup(request)