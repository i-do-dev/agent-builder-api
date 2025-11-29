from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from api.contracts.responses.user import UserSignUpResponse
from api.dependencies.auth import AuthSvc, AuthUserSvc, UserSignupSvc
from api.schemas.auth import Token, UserProfile
from api.contracts.requests.user import UserSignUpRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/token", response_model=Token)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: AuthSvc
) -> Token:
    return await auth.login(form_data.username, form_data.password)

""" @router.get("/me", response_model=UserProfileResponse)
async def me(auth_user: AuthUserSvc) -> UserProfileResponse:
    return auth_user """

@router.post("/register", response_model=UserSignUpResponse)
async def register(
    request: Annotated[UserSignUpRequest, Form()],
    auth_svc: AuthSvc,
    user_signup_svc: UserSignupSvc
) -> UserSignUpResponse:
    return await user_signup_svc.signup(request)