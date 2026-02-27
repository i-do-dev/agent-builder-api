from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class AgentCreateCommand:
    name: str
    api_name: str
    description: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None
    user_type: Optional[str] = None


@dataclass(frozen=True)
class AgentResult:
    id: UUID
    name: str
    api_name: str
    description: Optional[str]
    role: Optional[str]
    organization: Optional[str]
    user_type: Optional[str]
    modified_by: Optional[UUID]
    topics: list = field(default_factory=list)
