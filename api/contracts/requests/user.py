from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from api.contracts.user import UserData

class UserSignRequest(BaseModel):
    """Request contract for user authentication"""
    identifier: str = Field(..., description="Username or email address")
    password: str = Field(..., min_length=1, description="User's password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "identifier": "johndoe",
                "password": "securepassword123"
            }
        }

class UserSignUpRequest(UserData):
    """Request contract for user sign-up"""
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123",
                "confirm_password": "securepassword123"
            }
        }