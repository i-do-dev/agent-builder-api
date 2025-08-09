from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import models
from uuid import UUID
from schemas.topic_schemas import TopicCreateRequest
from schemas import topic_schemas
from schemas.topic_schemas import TopicResponse
from schemas.agent_schemas import AgentResponse  # Ensure this import is correct
from schemas.topic_schemas import TopicInstructionResponse  # Import the missing class


# Topic CRUD Operations
def create_topic(db: Session, topic: topic_schemas.TopicCreateRequest):
    try:
        topic_instructions = [
            models.TopicInstruction(instruction=instr) for instr in (topic.topic_instructions or [])
        ]
        topic_data = topic.model_dump(exclude={"topic_instructions"})
        db_topic = models.Topic(**topic_data, topic_instructions=topic_instructions)
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)
        return db_topic
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_topics(db: Session):
    topics = db.query(models.Topic).options(
        joinedload(models.Topic.topic_instructions)
    ).all()
    return [TopicResponse.model_validate(topic, from_attributes=True) for topic in topics]  # Convert to Pydantic

def get_topic(db, topic_id):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        return None
    
    return TopicResponse(
        id=topic.id,
        label=topic.label,
        classification_description=topic.classification_description,
        scope=topic.scope,
        agent=AgentResponse.model_validate(topic.agent),
        topic_instructions=[TopicInstructionResponse.model_validate(ti) for ti in topic.topic_instructions]
    )


def update_topic(db: Session, topic_id: UUID, topic: topic_schemas.TopicCreateRequest):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Update the topic fields
    db_topic.label = topic.label
    db_topic.classification_description = topic.classification_description
    db_topic.scope = topic.scope

    # Clear existing instructions and add new ones
    db_topic.topic_instructions.clear()
    for instruction in topic.topic_instructions or []:
        db_topic.topic_instructions.append(models.TopicInstruction(instruction=instruction))

    db.commit()
    db.refresh(db_topic)
    return db_topic

def delete_topic(db: Session, topic_id: UUID):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    db.delete(db_topic) 
    db.commit()
    return {"message": "Topic deleted successfully"}
