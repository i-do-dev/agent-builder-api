from sqlalchemy.orm import Session, joinedload
import models
from uuid import UUID
from schemas.agent_schemas import AgentCreateRequest
from schemas import agent_schemas

# Agent CRUD Operations
def create_agent(db: Session, agent: agent_schemas.AgentCreateRequest, user_id: UUID):
    db_agent = models.Agent(**agent.model_dump(), user_id=user_id)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def get_agents(db: Session):
    return db.query(models.Agent).options(
        joinedload(models.Agent.topics).joinedload(models.Topic.topic_instructions)
    ).all()

def get_agent(db: Session, agent_id: UUID):
    return db.query(models.Agent).options(
        joinedload(models.Agent.topics).joinedload(models.Topic.topic_instructions)
    ).filter(models.Agent.id == agent_id).first()

def update_agent(db: Session, agent_id: UUID, agent: agent_schemas.AgentUpdateRequest, current_user_id: UUID):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if db_agent:
        for key, value in agent.model_dump(exclude_unset=True).items():
            setattr(db_agent, key, value)
        db_agent.modified_by = current_user_id  # Update modified_by with the current user's ID
        db.commit()
        db.refresh(db_agent)
        return db_agent



# Agent CRUD Operations for delete
def delete_agent(db: Session, agent_id: str):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if db_agent:
        db.delete(db_agent)  # Cascading will handle deletion of topics and topic_instructions
        db.commit()
    else:
        raise ValueError("Agent not found")