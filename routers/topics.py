from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from crud import topic_crud as crud
from db_postgres import get_db
import models
from dependencies import get_current_user
from schemas import topic_schemas

router = APIRouter()

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
    topic = db.query(models.Topic).options(joinedload(models.Topic.agent)).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    if topic.agent.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this topic")
    db.delete(topic)
    db.commit()
    return {"message": "Topic deleted successfully"}
