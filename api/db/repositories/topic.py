from api.db.repositories.base import Repository
from api.db.models import Topic as TopicModel
from api.entities.topic import Topic as TopicEntity

class TopicRepository(Repository[TopicEntity, TopicModel]):
    """Repository for Topic model."""
    model = TopicModel