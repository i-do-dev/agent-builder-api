from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import models
from uuid import UUID
from schemas import agent_schemas
from db_neo4j import (
    add_agent, add_user_agent_relationship, update_agent as neo4j_update_agent,
    delete_agent as neo4j_delete_agent,delete_topic as neo4j_delete_topic,
    delete_topic_instruction as neo4j_delete_topic_instruction
)

"""
    Create Agent
    Create a new agent associated with a specific user in the database and sync to Neo4j.
    @urlParam db required for session
    @urlParam agent required AgentCreateRequest object containing agent data
    @urlParam user_id required The id of the user creating the agent Example: uuid
    @responseFile responses/agents/create_agent.json
    @response 400 {
        "errors": [
            "An agent with the name 'example' already exists for this user."
        ]
    }
    @response 500 {
        "errors": [
            "An error occurred while creating the agent: error_message"
        ]
    }
    @param db Session database session
    @param agent AgentCreateRequest agent creation request object
    @param user_id UUID the unique identifier of the user creating the agent
    @return Agent created agent object
"""
def create_agent(db: Session, agent: agent_schemas.AgentCreateRequest, user_id: UUID):
    # VALIDATION: Check for duplicate agent name for the same user ---
    # Query for an existing agent with the same name for this specific user
    existing_agent = db.query(models.Agent).filter(
        models.Agent.name == agent.name,
        models.Agent.user_id == user_id  # Ensure it's for the same user
    ).first()

    if existing_agent:
        raise HTTPException(
            status_code=400,
            detail=f"An agent with the name '{agent.name}' already exists for this user."
        )

    db_agent = models.Agent(**agent.model_dump(), user_id=user_id)
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)

    # Sync to Neo4j after successful insert into Postgres
    add_agent(
        agent_id=str(db_agent.id),
        name=db_agent.name,
        api_name=db_agent.api_name,
        description=db_agent.description,
        role=db_agent.role,
        organization=db_agent.organization,
        user_type=db_agent.user_type
    )
    # NEW: link this agent to its user in Neo4j
    add_user_agent_relationship(
        user_id=str(user_id),
        agent_id=str(db_agent.id)
    )
    return db_agent

"""
    Get All Agents
    Retrieve all agents with their associated user and topics including topic instructions from the database.
    @urlParam db required for session
    @responseFile responses/agents/get_agents.json
    @response 500 {
        "errors": [
            "An error occurred while retrieving agents: error_message"
        ]
    }
    @param db Session database session
    @return List[Agent] list of agent objects with user and topics
"""
def get_agents(db: Session):
    """Get all agents with their creator's name."""
    agents = db.query(models.Agent).options(
        joinedload(models.Agent.user),  # Load the user relationship
        joinedload(models.Agent.topics).joinedload(models.Topic.topic_instructions)
    ).all()
    # Manually set the creator_name for each agent
    for agent in agents:
        if agent.user:
            agent.creator_name = f"{agent.user.first_name} {agent.user.last_name}".strip()
        else:
            agent.creator_name = "Unknown User"
    return agents

"""
    Get Agent by ID
    Retrieve a specific agent by its ID with associated user and topics including topic instructions from the database.
    @urlParam db required for session
    @urlParam agent_id required The id of the agent to retrieve Example: uuid
    @responseFile responses/agents/get_agent_by_id.json
    @response 404 {
        "errors": [
            "Agent not found"
        ]
    }
    @response 500 {
        "errors": [
            "An error occurred while retrieving the agent: error_message"
        ]
    }
    @param db Session database session
    @param agent_id UUID the unique identifier of the agent to retrieve
    @return Agent agent object if found, None otherwise
"""
def get_agent(db: Session, agent_id: UUID):
    """Get a single agent by ID with its creator's name."""
    agent = db.query(models.Agent).options(
        joinedload(models.Agent.user),  # Load the user relationship
        joinedload(models.Agent.topics).joinedload(models.Topic.topic_instructions)
    ).filter(models.Agent.id == agent_id).first()
    
    if agent and agent.user:
        agent.creator_name = f"{agent.user.first_name} {agent.user.last_name}".strip()
    elif agent:
        agent.creator_name = "Unknown User"
    return agent

"""
    Update Agent
    Update an existing agent by its ID in the database and sync changes to Neo4j.
    @urlParam db required for session
    @urlParam agent_id required The id of the agent to update Example: uuid
    @urlParam agent required AgentUpdateRequest object containing update data
    @urlParam current_user_id required The id of the current user making the update Example: uuid
    @responseFile responses/agents/update_agent.json
    @response 400 {
        "errors": [
            "An agent with the name 'example' already exists for this user."
        ]
    }
    @response 404 {
        "errors": [
            "Agent not found"
        ]
    }
    @response 500 {
        "errors": [
            "An error occurred while updating the agent: error_message"
        ]
    }
    @param db Session database session
    @param agent_id UUID the unique identifier of the agent to update
    @param agent AgentUpdateRequest agent update request object
    @param current_user_id UUID the unique identifier of the current user
    @return Agent updated agent object
"""
def update_agent(db: Session, agent_id: UUID, agent: agent_schemas.AgentUpdateRequest, current_user_id: UUID):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    # Store old values before updating, in case they are not part of the update request
    old_name = db_agent.name
    old_api_name = db_agent.api_name
    old_description = db_agent.description
    old_role = db_agent.role
    old_organization = db_agent.organization
    old_user_type = db_agent.user_type
    # If the name is being updated, check for duplicates.
    new_name = agent.name if agent.name is not None else old_name # Determine the new name value

    if agent.name is not None and agent.name != old_name: # Only validate if name is changing
        # Query for an existing agent with the same *new* name for this specific user, excluding the current agent being updated
        existing_agent = db.query(models.Agent).filter(
            models.Agent.name == new_name,
            models.Agent.user_id == current_user_id,  # Same user
            models.Agent.id != agent_id  # Exclude the agent being updated itself
        ).first()

        if existing_agent:
            raise HTTPException(
                status_code=400,
                detail=f"An agent with the name '{new_name}' already exists for this user."
            )

    # Update the agent fields
    for key, value in agent.model_dump(exclude_unset=True).items():
        setattr(db_agent, key, value)

    db.commit()
    db.refresh(db_agent)

    # Use the updated values from db_agent, falling back to old values if not updated
    neo4j_update_agent(
        agent_id=str(db_agent.id),
        name=db_agent.name if db_agent.name is not None else old_name,
        api_name=db_agent.api_name if db_agent.api_name is not None else old_api_name,
        description=db_agent.description if db_agent.description is not None else old_description,
        role=db_agent.role if db_agent.role is not None else old_role,
        organization=db_agent.organization if db_agent.organization is not None else old_organization,
        user_type=db_agent.user_type if db_agent.user_type is not None else old_user_type
    )
    return db_agent

"""
    Delete Agent
    Delete an agent by its ID from the database and remove it from Neo4j along with all associated topics and their instructions.
    @urlParam db required for session
    @urlParam agent_id required The id of the agent to delete Example: uuid
    @responseFile responses/agents/delete_agent.json
    @response 404 {
        "errors": [
            "Agent not found"
        ]
    }
    @response 500 {
        "errors": [
            "An error occurred while deleting the agent: error_message"
        ]
    }
    @param db Session database session
    @param agent_id str the unique identifier of the agent to delete
    @return dict success message
"""
def delete_agent(db: Session, agent_id: str):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise ValueError("Agent not found")

    # First, get all topics associated with this agent
    topics_to_delete = db_agent.topics  # This uses the relationship defined in models
    # For each topic, delete its instructions and then the topic itself from Neo4j
    for topic in topics_to_delete:
        # Delete all instructions for this topic from Neo4j
        for instruction in topic.topic_instructions:
            neo4j_delete_topic_instruction(instruction_id=str(instruction.id))
        # Delete the topic from Neo4j
        neo4j_delete_topic(topic_id=str(topic.id))
    # Finally, delete the agent from Neo4j
    neo4j_delete_agent(agent_id=agent_id)

    db.delete(db_agent)
    db.commit()
    return {"message": "Agent deleted successfully"}
