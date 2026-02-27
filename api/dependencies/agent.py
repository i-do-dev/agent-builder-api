from typing import Annotated
from fastapi import Depends
from functools import lru_cache
from api.dependencies.db import Db
from src.handlers.commands.agent.create_agent import AgentCreateCommandHandler

@lru_cache()
def get_agent_service(
    db: Db
) -> AgentCreateCommandHandler:
    return AgentCreateCommandHandler(db)

Agent = Annotated[AgentCreateCommandHandler, Depends(get_agent_service)]

