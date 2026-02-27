from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import Topic as TopicModel
from src.core.entities.topic import Topic as TopicEntity
from src.adapters.db.mappers.topic import TopicMapper

class TopicRepository(Repository[TopicEntity, TopicModel]):
    """Repository for Topic model."""
    model = TopicModel

    async def _model_to_entity(self, model: TopicModel) -> TopicEntity:
        return TopicMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: TopicEntity) -> TopicModel:
        return TopicMapper.entity_to_model(entity)