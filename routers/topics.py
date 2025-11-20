from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from crud import topic_crud as crud
from db_postgres import get_db
import models
from dependencies import get_current_user
from schemas import topic_schemas

router = APIRouter()    

"""
Create Topic
API endpoint to create a new topic in the system.
Validates user authentication and creates topic in both PostgreSQL and Neo4j databases.
@responseFile responses/topics/create_topic.json
@param topic TopicCreateRequest The topic creation request containing topic details
@param db Session Database session dependency for PostgreSQL operations
@param current_user User Currently authenticated user from token validation
@return Topic The created topic object
"""
@router.post("/topics/", response_model=topic_schemas.TopicResponse)
def create_topic(
    topic: topic_schemas.TopicCreateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_topic(db, topic)

@router.get("/topics/", response_model=topic_schemas.TopicsResponse)
def get_topics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    topics = crud.get_topics(db)
    return {"topics": topics}

@router.get("/topics/{topic_id}", response_model=topic_schemas.TopicResponse)
def get_topic_by_id(
    topic_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    topic = crud.get_topic(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic {topic_id} not found")
    return topic

@router.put("/topics/{topic_id}", response_model=topic_schemas.TopicResponse)
def update_topic(
    topic_id: str,
    topic: topic_schemas.TopicUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.update_topic(db, topic_id, topic)

@router.delete("/topics/{topic_id}", response_model=dict)
def delete_topic(
    topic_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = crud.delete_topic(db, topic_id)
    return result
