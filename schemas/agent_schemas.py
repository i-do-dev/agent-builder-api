from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from schemas.topic_schemas import TopicCreateRequest, TopicResponse

class AgentBase(BaseModel):
    name: str
    api_name: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None
    user_type: Optional[str] = None
    topics: Optional[List[TopicCreateRequest]] = []

class AgentCreateRequest(AgentBase):
    pass

class AgentUpdateRequest(AgentBase):
    pass    

class AgentResponse(AgentBase):
    id: UUID
    user_id: UUID
    topics: List[TopicResponse] = []
    creator_name: Optional[str] = None
    
    class Config:
        from_attributes = True


AgentResponse.model_rebuild()
