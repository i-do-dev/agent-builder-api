from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class TopicCreateCommand:
    label: str
    classification_description: Optional[str] = None
    instructions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class TopicResult:
    id: UUID
    label: str
    classification_description: Optional[str] = None
    instructions: list = field(default_factory=list)
    agent: Optional[dict] = None
