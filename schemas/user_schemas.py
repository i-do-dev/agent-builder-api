from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from schemas.agent_schemas import AgentResponse, AgentCreateRequest

# User Schemas
class UserBase(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreateRequest(UserBase):
    password: str
    confirm_password: str 
    agents: Optional[List[AgentCreateRequest]] = []

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    agents: List[AgentResponse] = []

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    first_name: Optional[str]
    last_name: Optional[str]

UserResponse.model_rebuild()
