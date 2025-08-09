from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from schemas.topic_schemas import TopicCreateRequest, TopicResponse

#  Agent Base Schema
class AgentBase(BaseModel):
    name: str
    api_name: str
    description: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None
    user_type: Optional[str] = None  # Dropdown value
    topics: Optional[List[TopicCreateRequest]] = []

# Schema for creating an agent
class AgentCreateRequest(AgentBase):
    pass

class AgentUpdateRequest(AgentBase):
    pass    

#  Response schema for an agent
class AgentResponse(AgentBase):
    id: UUID
    user_id: UUID
    modified_by: Optional[UUID] = None
    topics: List[TopicResponse] = []

    class Config:
        from_attributes = True

#  Rebuild models to resolve forward references
AgentResponse.model_rebuild()
