from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Optional, List, TYPE_CHECKING

# Only import for type checking to avoid circular imports
if TYPE_CHECKING:
    from api.entities.topic import Topic
    from api.entities.user import UserEntity

@dataclass
class Agent:
    """Agent domain entity representing the core business object"""
    id: UUID | None = field(default=None)
    name: str | None = field(default=None)
    api_name: str | None = field(default=None)
    description: str | None = field(default=None)
    role: str | None = field(default=None)
    organization: str | None = field(default=None)
    user_type: str | None = field(default=None)
    user_id: UUID | None = field(default=None)
    created_at: datetime | None = field(default=None)
    is_active: bool = True
    
    def __str__(self) -> str:
        """String representation of the agent"""
        return f"Agent(name='{self.name}', api_name='{self.api_name}', user_id='{self.user_id}')"

@dataclass
class AgentWithTopics(Agent):
    """Agent entity with topics relationship loaded"""
    topics: List['Topic'] = field(default_factory=list)
    
    def add_topic(self, topic: 'Topic') -> None:
        """Add a topic to the agent"""
        if topic not in self.topics:
            self.topics.append(topic)
    
    def remove_topic(self, topic: 'Topic') -> None:
        """Remove a topic from the agent"""
        if topic in self.topics:
            self.topics.remove(topic)
    
    def get_topic_count(self) -> int:
        """Get number of topics associated with the agent"""
        return len(self.topics)
    
    def has_topics(self) -> bool:
        """Check if agent has any topics"""
        return len(self.topics) > 0

@dataclass
class AgentWithUser(Agent):
    """Agent entity with user relationship loaded"""
    user: Optional['UserEntity'] = field(default=None)
    
    def get_owner_name(self) -> str:
        """Get the owner's name if user is loaded"""
        if self.user:
            return self.user.get_full_name()
        return "Unknown User"