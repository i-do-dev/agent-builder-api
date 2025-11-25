from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from api.contracts.user import UserData

class CreateUserRequest(BaseModel):
    """Request contract for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name")
    password: str = Field(..., min_length=8, description="User's password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123"
            }
        }

class LoginRequest(BaseModel):
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

class UpdateUserRequest(BaseModel):
    """Request contract for updating user profile"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Smith"
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