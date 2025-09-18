from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_postgres import get_db
from dependencies import get_current_user
import models
from schemas import agent_schemas
from crud import agent_crud as crud
from schemas import topic_schemas

router = APIRouter()

@router.post("/agents/", response_model=agent_schemas.AgentResponse)
def create_agent(
    agent: agent_schemas.AgentCreateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_agent(db, agent, user_id=current_user.id)

@router.get("/agents/", response_model=list[agent_schemas.AgentResponse])
def get_agents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    agents = crud.get_agents(db)
    # Populate creator information if not already done
    for agent in agents:
        agent.creator_name = f"{agent.user.first_name} {agent.user.last_name}"   
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
