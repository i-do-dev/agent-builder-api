from pydantic import BaseModel
from uuid import UUID

class TopicInstructionBase(BaseModel):
    instruction: str

class TopicInstructionCreate(TopicInstructionBase):
    topic_id: UUID

class TopicInstructionResponse(TopicInstructionBase):
    id: UUID
    topic_id: UUID

    class Config:
        from_attributes = True
