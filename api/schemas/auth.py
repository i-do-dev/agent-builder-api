from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    exp: int

class UserData(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

class UserDataWithPassword(UserData):
    password: str = Field(..., min_length=8)

class UserProfile(UserData):
    id: UUID
    created_at: str | None = None

class UserAuth(UserDataWithPassword):
    id: UUID
    created_at: str | None = None

class UserSignUpRequest(UserData):
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)