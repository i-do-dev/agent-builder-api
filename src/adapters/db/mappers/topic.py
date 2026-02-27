from src.adapters.db.models import Topic as TopicModel
from src.core.entities.topic import Topic as TopicEntity


class TopicMapper:
    @staticmethod
    def model_to_entity(model: TopicModel) -> TopicEntity:
        return TopicEntity(
            id=model.id,
            label=model.label,
            classification_description=model.classification_description,
            agent_id=model.agent_id,
            created_at=model.created_at,
        )

    @staticmethod
    def entity_to_model(entity: TopicEntity) -> TopicModel:
        kwargs = {
            "label": entity.label,
            "classification_description": entity.classification_description,
            "agent_id": entity.agent_id,
        }
        if entity.id is not None:
            kwargs["id"] = entity.id
        return TopicModel(**kwargs)
