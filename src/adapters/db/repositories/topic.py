from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import Topic as TopicModel
from src.core.entities.topic import Topic as TopicEntity

class TopicRepository(Repository[TopicEntity, TopicModel]):
    """Repository for Topic model."""
    model = TopicModel