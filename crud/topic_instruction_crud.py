from sqlalchemy.orm import Session
import models
from uuid import UUID
from schemas import topic_instruction_schemas

# Topic Instruction CRUD Operations
def create_instruction(db: Session, instruction: topic_instruction_schemas.TopicInstructionCreate):
    db_instruction = models.TopicInstruction(**instruction.model_dump())
    db.add(db_instruction)
    db.commit()
    db.refresh(db_instruction)
    return db_instruction

def get_instructions(db: Session):
    return db.query(models.TopicInstruction).all()

def get_instruction_by_id(db: Session, instruction_id: UUID):
    return db.query(models.TopicInstruction).filter(models.TopicInstruction.id == instruction_id).first()
