from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserData(BaseModel):
    """ Basic user data contract """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

class UserProfile(UserData):
    """ Public user profile contract """
    id: UUID
    created_at: str | None = None

class UserProfileNoKey(UserData):
    """ Public user profile contract without key """
    joined_at: str | None = None

class UserDataWithPassword(UserData):
    """ User contract for authentication including password """
    password: str = Field(..., min_length=8)
