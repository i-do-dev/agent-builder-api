from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import Agent as AgentModel
from src.core.entities.agent import Agent as AgentEntity
from src.adapters.db.mappers.agent import AgentMapper

class AgentRepository(Repository[AgentEntity, AgentModel]):
    """Repository for Agent model."""
    model = AgentModel

    async def _model_to_entity(self, model: AgentModel) -> AgentEntity:
        return AgentMapper.model_to_entity(model)

    async def _entity_to_model(self, entity: AgentEntity) -> AgentModel:
        return AgentMapper.entity_to_model(entity)