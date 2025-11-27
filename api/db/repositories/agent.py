from sqlalchemy import select, or_
from typing import Optional

from sqlalchemy import or_
from api.db.repositories.base import Repository
from api.db.models import Agent as AgentModel
from api.entities.agent import Agent as AgentEntity

class AgentRepository(Repository[AgentEntity, AgentModel]):
    """Repository for Agent model."""
    model = AgentModel