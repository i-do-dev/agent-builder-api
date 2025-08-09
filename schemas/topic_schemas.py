from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Optional
from schemas.topic_instruction_schemas import TopicInstructionResponse

class AgentResponse(BaseModel):
    id: UUID
    name: str
    user_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class TopicResponse(BaseModel):
    id: UUID
    agent: AgentResponse
    label: str
    classification_description: Optional[str] = None
    scope: Optional[str] = None
    topic_instructions: List[TopicInstructionResponse] = []


    model_config = ConfigDict(from_attributes=True)


# Topic Schemas
class TopicBase(BaseModel):
    label: str
    classification_description: Optional[str] = None
    scope: Optional[str] = None
    topic_instructions: Optional[List[str]] = []

class TopicCreateRequest(TopicBase):
    agent_id: Optional[UUID] = None
    topic_instructions: Optional[List[str]] = []

class TopicUpdateRequest(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: UUID
    topic_instructions: List[TopicInstructionResponse] = []
    agent: Optional[AgentResponse] = None  # Include the agent relationship


    class Config:
        from_attributes = True

# New response model for multiple topics
class TopicsResponse(BaseModel):
    topics: List[TopicResponse]  # Ensure API returns {"topics": [...]}

# Rebuild models
TopicResponse.model_rebuild()
