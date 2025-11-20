from typing import Annotated
from fastapi import Depends
from functools import lru_cache
from api.dependencies.db import Db
from api.services.agent import AgentService

@lru_cache()
def get_agent_service(
    db: Db
) -> AgentService:
    return AgentService(db)

Agent = Annotated[AgentService, Depends(get_agent_service)]

