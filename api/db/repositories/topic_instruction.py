from api.db.repositories.base import Repository
from api.db.models import TopicInstruction as TopicInstructionModel
from api.entities.topic_instruction import TopicInstruction as TopicInstructionEntity

class TopicInstructionRepository(Repository[TopicInstructionEntity, TopicInstructionModel]):
    """Repository for TopicInstruction model."""
    model = TopicInstructionModel