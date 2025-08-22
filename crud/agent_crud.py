from sqlalchemy.orm import Session, joinedload
import models
from uuid import UUID
from schemas.agent_schemas import AgentCreateRequest
from schemas import agent_schemas
from db_neo4j import add_agent, add_user_agent_relationship

# Agent CRUD Operations
def create_agent(db: Session, agent: agent_schemas.AgentCreateRequest, user_id: UUID):
    db_agent = models.Agent(**agent.model_dump(), user_id=user_id)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)

    # ✅ Sync to Neo4j after successful insert into Postgres
    add_agent(
        agent_id=str(db_agent.id),
        name=db_agent.name,
        api_name=db_agent.api_name,
        description=db_agent.description,
        role=db_agent.role,
        organization=db_agent.organization,
        user_type=db_agent.user_type
    )

    # 🟢 NEW: link this agent to its user in Neo4j
    add_user_agent_relationship(
        user_id=str(user_id),
        agent_id=str(db_agent.id)
        )
    
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
        db_agent.modified_by = current_user_id
        db.commit()
        db.refresh(db_agent)
        return db_agent

def delete_agent(db: Session, agent_id: str):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if db_agent:
        db.delete(db_agent)
        db.commit()
    else:
        raise ValueError("Agent not found")
        
