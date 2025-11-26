from pydantic import BaseModel, Field
from api.contracts.user import UserProfile

class UserSignUpResponse(UserProfile):
    """User sign-up response contract"""
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created_at": "2023-01-01T00:00:00Z"
            }
        }