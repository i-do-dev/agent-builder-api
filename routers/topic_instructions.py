from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_current_user
from database import get_db
import models
from schemas import topic_instruction_schemas
from crud import topic_instruction_crud as crud
router = APIRouter()

@router.post("/topic_instructions/", response_model=topic_instruction_schemas.TopicInstructionResponse)
def create_instruction(
    instruction: topic_instruction_schemas.TopicInstructionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_instruction(db, instruction)

@router.get("/topic_instructions/", response_model=list[topic_instruction_schemas.TopicInstructionResponse])
def get_instructions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_instructions(db)

@router.get("/topic_instructions/{instruction_id}", response_model=topic_instruction_schemas.TopicInstructionResponse)
def get_instruction_by_id(
    instruction_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    instruction = crud.get_instruction_by_id(db, instruction_id)
    if not instruction:
        raise HTTPException(
            status_code=404,
            detail=f"Instruction {instruction_id} not found"
        )
    return instruction
