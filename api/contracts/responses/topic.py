from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from api.contracts.responses.topic_instruction import TopicInstructionResponse


class AgentResponse(BaseModel):
    id: UUID
    name: str
    user_id: UUID


class TopicBase(BaseModel):
    label: str
    classification_description: Optional[str] = None
    scope: Optional[str] = None
    topic_instructions: Optional[List[str]] = []


class TopicResponse(TopicBase):
    id: UUID
    instructions: List[TopicInstructionResponse] = []
    agent: Optional[AgentResponse] = None

    class Config:
        from_attributes = True


class TopicsResponse(BaseModel):
    topics: List[TopicResponse]


TopicResponse.model_rebuild()
