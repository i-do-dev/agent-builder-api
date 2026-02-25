from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import TopicInstruction as TopicInstructionModel
from src.core.entities.topic_instruction import TopicInstruction as TopicInstructionEntity

class TopicInstructionRepository(Repository[TopicInstructionEntity, TopicInstructionModel]):
    """Repository for TopicInstruction model."""
    model = TopicInstructionModel