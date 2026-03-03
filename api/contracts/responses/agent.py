from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from api.contracts.responses.topic import TopicResponse


class AgentBase(BaseModel):
    name: str
    api_name: str
    description: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None
    user_type: Optional[str] = None


class AgentResponse(AgentBase):
    id: UUID
    modified_by: Optional[UUID] = None
    topics: List[TopicResponse] = []

    class Config:
        from_attributes = True


AgentResponse.model_rebuild()
