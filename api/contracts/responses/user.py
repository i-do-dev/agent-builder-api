from pydantic import BaseModel, Field
from api.contracts.user import UserProfileNoKey

class UserSignUpResponse(UserProfileNoKey):
    """User sign-up response contract"""
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created_at": "2023-01-01T00:00:00Z"
            }
        }

class UserProfileResponse(UserProfileNoKey):
    """User profile response contract"""
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created_at": "2023-01-01T00:00:00Z"
            }
        }