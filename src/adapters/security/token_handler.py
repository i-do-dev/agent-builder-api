from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from src.core.services.token_handler import ITokenHandler, TokenPayload
from settings import Settings


class TokenHandler(ITokenHandler):
    def __init__(self, settings: Settings):
        self.secret_key = settings.secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        data_to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        data_to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(data_to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str | None = payload.get("sub")
            exp: int | None = payload.get("exp")
            if username is None or exp is None:
                raise ValueError("Could not validate credentials")
            return TokenPayload(sub=username, exp=exp)
        except InvalidTokenError as exc:
            raise ValueError("Could not validate credentials") from exc
