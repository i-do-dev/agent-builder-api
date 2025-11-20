from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Optional
from schemas.topic_instruction_schemas import TopicInstructionResponse

class AgentResponse(BaseModel):
    id: UUID
    name: str
    user_id: UUID
    model_config = ConfigDict(from_attributes=True)

class TopicBase(BaseModel):
    label: str
    classification_description: Optional[str] = None
    scope: Optional[str] = None
    topic_instructions: Optional[List[str]] = []

class TopicCreateRequest(TopicBase):
    agent_id: UUID
    topic_instructions: Optional[List[str]] = []

class TopicUpdateRequest(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: UUID
    topic_instructions: List[TopicInstructionResponse] = []
    # Optional because sometimes we might not want to nest the agent details
    agent: Optional[AgentResponse] = None
    class Config:
        from_attributes = True

class TopicsResponse(BaseModel):
    topics: List[TopicResponse]

TopicResponse.model_rebuild()