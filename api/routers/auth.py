from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from api.dependencies.auth import Auth, AuthUser
from api.schemas.auth import Token, UserProfile, UserSignUpRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/token", response_model=Token)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: Auth
) -> Token:
    return await auth.login(form_data.username, form_data.password)

@router.get("/me", response_model=UserProfile)
async def me(user: AuthUser) -> UserProfile:
    return user

@router.post("/register", response_model=UserProfile)
async def register(
    form_data: Annotated[UserSignUpRequest, Form()],
    auth: Auth
) -> UserProfile:
    return await auth.register(form_data)