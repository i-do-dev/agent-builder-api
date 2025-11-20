from sqlalchemy import select, or_
from typing import Optional

from sqlalchemy import or_
from api.db.repositories.base import Repository
from api.db.models import Agent

class AgentRepository(Repository[Agent]):
    """Repository for Agent model."""
    model = Agent
