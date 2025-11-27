# api/entities/topic_instruction.py
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Optional, TYPE_CHECKING

# Only import for type checking to avoid circular imports
if TYPE_CHECKING:
    from api.entities.topic import Topic

@dataclass
class TopicInstruction:
    """TopicInstruction domain entity representing an instruction within a topic"""
    id: UUID | None = field(default=None)
    instruction: str | None = field(default=None)
    topic_id: UUID | None = field(default=None)
    created_at: datetime | None = field(default=None)
    is_active: bool = True
    
    def update_instruction(self, instruction: str) -> None:
        """Update instruction content"""
        if not instruction or not instruction.strip():
            raise ValueError("Instruction cannot be empty")
        self.instruction = instruction.strip()
    
    def __str__(self) -> str:
        """String representation of the instruction"""
        preview = self.get_instruction_preview(50)
        return f"TopicInstruction(id='{self.id}', preview='{preview}')"

@dataclass
class TopicInstructionWithTopic(TopicInstruction):
    """TopicInstruction entity with topic relationship loaded"""
    topic: Optional['Topic'] = field(default=None)
    
    def get_topic_label(self) -> str:
        """Get the topic's label if topic is loaded"""
        if self.topic:
            return self.topic.label
        return "Unknown Topic"
