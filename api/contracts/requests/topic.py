from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List


class TopicBase(BaseModel):
    label: str
    classification_description: Optional[str] = None
    scope: Optional[str] = None
    topic_instructions: Optional[List[str]] = []


class TopicCreateRequest(TopicBase):
    agent_id: Optional[UUID] = None
    instructions: Optional[List[str]] = []


class TopicUpdateRequest(TopicBase):
    pass
