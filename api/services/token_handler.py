from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from api.schemas.auth import TokenPayload
from api.settings import Settings

class TokenHandler:
    """Service for handling JWT token creation and verification."""
    
    def __init__(self, settings: Settings = None):        
        self.secret_key = settings.secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        data_to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        data_to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(data_to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode(self, token: str) -> TokenPayload:
        """Decode and verify a JWT token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            exp: int = payload.get("exp")
            if username is None or exp is None:
                raise credentials_exception
            return TokenPayload(sub=username, exp=exp)
        except InvalidTokenError:
            raise credentials_exception
