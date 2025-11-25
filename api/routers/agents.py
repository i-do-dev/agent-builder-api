from fastapi import APIRouter
from api.dependencies.agent import Agent
from api.dependencies.common import BearerToken, TokenSvc
from api.schemas.agent import AgentCreateRequest, AgentResponse
from api.schemas.auth import TokenPayload

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

@router.post("/")
async def create(
        bearer_token: BearerToken, 
        token_svc: TokenSvc, 
        agent: Agent, 
        agent_req: AgentCreateRequest
    ) -> AgentResponse:
    token_payload: TokenPayload = token_svc.decode(bearer_token)
    return await agent.create_on_request(agent_req, token_payload.sub)

""" 
@router.get("/agents/", response_model=list[agent_schemas.AgentResponse])
def get_agents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_agents(db)

@router.get("/agents/{agent_id}", response_model=agent_schemas.AgentResponse)
def get_agent_by_id(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    agent = crud.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    return agent

@router.get("/agents/{agent_id}/topics", response_model=list[topic_schemas.TopicResponse])
def get_agent_topics(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    agent = crud.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.topics

@router.put("/agents/{agent_id}", response_model=agent_schemas.AgentResponse)
def update_agent(
    agent_id: str,
    agent: agent_schemas.AgentUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.update_agent(db, agent_id, agent, current_user.id)

@router.delete("/agents/{agent_id}", response_model=dict)
def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    agent = crud.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this agent")
    crud.delete_agent(db, agent_id)
    return {"message": "Agent deleted successfully"}
 """