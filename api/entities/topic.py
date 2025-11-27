# api/entities/topic.py
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING, Optional, List

# Only import for type checking to avoid circular imports
if TYPE_CHECKING:
    from api.entities.agent import Agent
    from api.entities.topic_instruction import TopicInstruction

@dataclass
class Topic:
    """Topic domain entity representing a topic within an agent"""
    id: UUID | None = field(default=None)
    label: str | None = field(default=None)
    classification_description: str | None = field(default=None)
    agent_id: UUID | None = field(default=None)
    created_at: datetime | None = field(default=None)
    is_active: bool = True
    
    # Business methods
    def is_owned_by_agent(self, agent_id: UUID) -> bool:
        """Check if topic belongs to specific agent"""
        return self.agent_id == agent_id
    
    def __str__(self) -> str:
        """String representation of the topic"""
        return f"Topic(label='{self.label}', agent_id='{self.agent_id}')"

@dataclass
class TopicWithInstructions(Topic):
    """Topic entity with instructions relationship loaded"""
    instructions: List['TopicInstruction'] = field(default_factory=list)
    
    def add_instruction(self, instruction: 'TopicInstruction') -> None:
        """Add an instruction to the topic"""
        if instruction not in self.instructions:
            self.instructions.append(instruction)
    
    def remove_instruction(self, instruction: 'TopicInstruction') -> None:
        """Remove an instruction from the topic"""
        if instruction in self.instructions:
            self.instructions.remove(instruction)
    
    def get_instruction_count(self) -> int:
        """Get number of instructions associated with the topic"""
        return len(self.instructions)
    
    def has_instructions(self) -> bool:
        """Check if topic has any instructions"""
        return len(self.instructions) > 0

@dataclass
class TopicWithAgent(Topic):
    """Topic entity with agent relationship loaded"""
    agent: Optional['Agent'] = field(default=None)
    
    def get_agent_name(self) -> str:
        """Get the agent's name if agent is loaded"""
        if self.agent:
            return self.agent.name
        return "Unknown Agent"
    
    def get_agent_api_name(self) -> str:
        """Get the agent's API name if agent is loaded"""
        if self.agent:
            return self.agent.api_name
        return "unknown-agent"
    
    def is_agent_active(self) -> bool:
        """Check if the parent agent is active"""
        if self.agent:
            return self.agent.is_active
        return False
