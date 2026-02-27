from functools import lru_cache
from typing import Annotated
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from src.adapters.security.token_handler import TokenHandler
from src.core.services.token_handler import ITokenHandler
from settings import Settings

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def get_token_service() -> ITokenHandler:
    return TokenHandler(get_settings())

TokenSvc = Annotated[ITokenHandler, Depends(get_token_service)]
oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
BearerToken = Annotated[str, Depends(oauth_scheme)]


