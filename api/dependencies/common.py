from functools import lru_cache
from typing import Annotated
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from api.services.token import TokenService
from api.settings import Settings

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def get_token_service() -> TokenService:
    return TokenService(get_settings())

Token = Annotated[TokenService, Depends(get_token_service)]
oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
BearerToken = Annotated[str, Depends(oauth_scheme)]


