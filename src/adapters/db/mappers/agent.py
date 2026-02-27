from src.adapters.db.models import Agent as AgentModel
from src.core.entities.agent import Agent as AgentEntity


class AgentMapper:
    @staticmethod
    def model_to_entity(model: AgentModel) -> AgentEntity:
        return AgentEntity(
            id=model.id,
            name=model.name,
            api_name=model.api_name,
            description=model.description,
            role=model.role,
            organization=model.organization,
            user_type=model.user_type,
            user_id=model.user_id,
            created_at=model.created_at,
        )

    @staticmethod
    def entity_to_model(entity: AgentEntity) -> AgentModel:
        kwargs = {
            "name": entity.name,
            "api_name": entity.api_name,
            "description": entity.description,
            "role": entity.role,
            "organization": entity.organization,
            "user_type": entity.user_type,
            "user_id": entity.user_id,
        }
        if entity.id is not None:
            kwargs["id"] = entity.id
        return AgentModel(**kwargs)
