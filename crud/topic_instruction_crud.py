from sqlalchemy.orm import Session
import models
from uuid import UUID
from schemas import topic_instruction_schemas
from db_neo4j import add_topic_instruction ,add_topic_topic_instruction_relationship

# Topic Instruction CRUD Operations
def create_instruction(db: Session, instruction: topic_instruction_schemas.TopicInstructionCreate):
    db_instruction = models.TopicInstruction(**instruction.model_dump())
    db.add(db_instruction)
    db.commit()
    db.refresh(db_instruction)

    # ✅ Sync to Neo4j after successful insert into Postgres
    add_topic_instruction(
        topic_id=str(db_instruction.topic_id),
        instruction_id=str(db_instruction.id),
        instruction_text=db_instruction.instruction
    )

    # 🟢 NEW: link this topic to its agent in Neo4j
    add_topic_topic_instruction_relationship(
        topic_id=str(db_instruction.topic_id),
        instruction_id=str(db_instruction.id)
    )
    
    return db_instruction

def get_instructions(db: Session):
    return db.query(models.TopicInstruction).all()

def get_instruction_by_id(db: Session, instruction_id: UUID):
    return db.query(models.TopicInstruction).filter(models.TopicInstruction.id == instruction_id).first()
