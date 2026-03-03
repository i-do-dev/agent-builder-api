from pydantic import BaseModel
from typing import Optional, List
from api.contracts.requests.topic import TopicCreateRequest


class AgentBase(BaseModel):
    name: str
    api_name: str
    description: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None
    user_type: Optional[str] = None
    topics: Optional[List[TopicCreateRequest]] = []


class AgentCreateRequest(AgentBase):
    pass


class AgentUpdateRequest(AgentBase):
    pass
