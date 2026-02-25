from sqlalchemy import select, or_
from typing import Optional

from sqlalchemy import or_
from src.adapters.db.repositories.base import Repository
from src.adapters.db.models import Agent as AgentModel
from src.core.entities.agent import Agent as AgentEntity

class AgentRepository(Repository[AgentEntity, AgentModel]):
    """Repository for Agent model."""
    model = AgentModel