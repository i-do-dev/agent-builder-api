from api.dependencies.db import Db
from api.schemas.agent import AgentCreateRequest, AgentResponse
from api.db.models import Agent

class AgentCreator:
    """Handles the creation of an agent based on a request."""

    def __init__(self, db: Db, username: str):
        self.db = db
        self.username = username

    async def on_request(self, agent_req: AgentCreateRequest) -> AgentResponse:
        user = await self.db.user.get_by_username(self.username)
        if not user:
            raise ValueError("User not found")
        
        agent_model = Agent(
            name=agent_req.name,
            api_name=agent_req.api_name,
            description=agent_req.description,
            role=agent_req.role,
            organization=agent_req.organization,
            user_type=agent_req.user_type,
            user_id=user.id
        )

        agent: Agent = await self.create(agent_model)
        return AgentResponse(
            id=agent.id,
            name=agent.name,
            api_name=agent.api_name,
            description=agent.description,
            role=agent.role,
            organization=agent.organization,
            user_type=agent.user_type,
            modified_by=user.id,
        )
    
    async def create(self, agent: Agent) -> Agent:
        return await self.db.agent.add(agent)
        

class AgentService:
    """Service for handling agent."""
    
    def __init__(self, db: Db):
        self.db = db

    async def create_on_request(self, agent_req: AgentCreateRequest, username: str) -> AgentResponse:
        agent_creator = AgentCreator(self.db, username)
        response = await agent_creator.on_request(agent_req)
        return response