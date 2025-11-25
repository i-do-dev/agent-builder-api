from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid
from api.contracts.user import UserProfile

class UserResponse(BaseModel):
    """Base user response contract"""
    id: uuid.UUID = Field(..., description="Unique user identifier")
    username: str = Field(..., description="User's username")
    email: str = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    full_name: str = Field(..., description="User's full name")
    created_at: datetime = Field(..., description="Account creation timestamp")
    is_active: bool = Field(..., description="Whether the user account is active")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "created_at": "2023-01-01T00:00:00Z",
                "is_active": True
            }
        }

class UserAuthResponse(UserResponse):
    """User response for authentication scenarios (includes sensitive data)"""
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    permissions: list[str] = Field(default_factory=list, description="User permissions")

class UserProfileResponse(UserProfile):
    """Public user profile response (no sensitive data)"""
    full_name: str = Field(..., description="User's full name")
    
    class Config:
        from_attributes = True