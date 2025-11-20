from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import models, db_postgres
import os

# Secret key & algorithm
SECRET_KEY = os.getenv("JWT_SECRET", "fallback-secret")
ALGORITHM = "HS256"

# In-memory token blacklist
TOKEN_BLACKLIST = set()

# Must match login route mounted at /api/users/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def authenticate_user(token: str, db: Session):
    # Reject if token is blacklisted
    if token in TOKEN_BLACKLIST:
        raise HTTPException(status_code=401, detail="Token has been revoked. Please log in again.")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: 'sub' missing")

        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token error: {str(e)}")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(db_postgres.get_db)
) -> models.User:
    return authenticate_user(token, db)

def get_current_user_from_body_user_id(
    request_data: dict,
    db: Session = Depends(db_postgres.get_db)
) -> models.User:
    """
    This dependency validates the user_id from the request body and returns the authenticated user.
    It fetches the user's active token from the database and validates it.
    """
    user_id = request_data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required in request body")

    # Fetch the user from the database
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or invalid user_id")

    # Check if user has an active token
    if not user.access_token:
        raise HTTPException(status_code=401, detail="No active token found for user. Please log in again.")

    # Validate the token (check blacklist and decode)
    token = user.access_token
    if token in TOKEN_BLACKLIST:
        raise HTTPException(status_code=401, detail="Token has been revoked. Please log in again.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_user_id: str = payload.get("sub")
        if not token_user_id or str(token_user_id) != str(user_id):
            raise HTTPException(status_code=401, detail="Invalid token or token mismatch.")
        return user
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")
