from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserProfile(BaseModel):
    id: UUID
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    created_at: str | None = None

class UserAuth(UserProfile):
    password: str

class UserSignUpRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)