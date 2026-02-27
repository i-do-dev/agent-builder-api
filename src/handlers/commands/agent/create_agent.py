from src.adapters.db.uow import UnitOfWork
from src.core.entities.agent import Agent
from src.handlers.contracts.agent import AgentCreateCommand, AgentResult
from src.handlers.errors import NotFoundError


class AgentCreateCommandHandler:
    def __init__(self, db: UnitOfWork):
        self.db = db

    async def create_on_request(self, command: AgentCreateCommand, username: str) -> AgentResult:
        user = await self.db.user.get_by_username(username)
        if not user:
            raise NotFoundError("User not found")

        entity = Agent(
            name=command.name,
            api_name=command.api_name,
            description=command.description,
            role=command.role,
            organization=command.organization,
            user_type=command.user_type,
            user_id=user.id,
        )
        agent = await self.db.agent.add(entity)
        return AgentResult(
            id=agent.id,
            name=agent.name,
            api_name=agent.api_name,
            description=agent.description,
            role=agent.role,
            organization=agent.organization,
            user_type=agent.user_type,
            modified_by=user.id,
        )
