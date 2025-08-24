from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db_postgres import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError
from schemas import user_schemas
from crud import user_crud as crud
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_current_user
import os

# === Config ===
SECRET_KEY = os.getenv("JWT_SECRET", "fallback-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# === Setup ===
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# === Token Utility ===
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# === Static routes should go FIRST ===
@router.get("/users/validate-token")
def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "payload": payload}
    except JWTError:
        return {"valid": False}

# === User CRUD routes ===
@router.post("/users/", response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreateRequest, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@router.post("/users/login", response_model=user_schemas.TokenResponse)
def login_user(user_credentials: user_schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_credentials.email)
    if not user or not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "first_name": user.first_name,
        "last_name": user.last_name
    }

# === Protected routes ===
@router.get("/users/", response_model=list[user_schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user: user_schemas.UserResponse = Depends(get_current_user)):
    return crud.get_users(db)

@router.get("/users/{user_id}", response_model=user_schemas.UserResponse)
def get_user_by_id(user_id: str, db: Session = Depends(get_db), current_user: user_schemas.UserResponse = Depends(get_current_user)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"User {user_id} does not exist"
            }
        )
    return user
