from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import models
from uuid import UUID
from passlib.context import CryptContext
from schemas import user_schemas
from crud.agent_crud import create_agent
from db_neo4j import add_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User CRUD Operations
def create_user(db: Session, user: user_schemas.UserCreateRequest):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
            
    # Sync to Neo4j after successful insert into Postgres
    add_user( 
        user_id=str(db_user.id),
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email,
        password=hashed_password,
        user_type="user"
    )        
    
    if user.agents:
        for agent_data in user.agents:
            agent_data.user_id = db_user.id
            create_agent(db, agent_data, db_user.id)
     
    return db_user

"""
    Update User Token
    Update the user access_token in the db w.r.t. to the specified userId. 
    @urlParam db required for session 
    @urlParam user_id required The id of a users Example: uuid
    @urlParam token required The acceess_token of a user Example: JWT Token 
    @responseFile responses/users/update_user_token.json
    @response 400 {
    "errors": [
        "User not found."
      ]
     }
    @param db mix
    @param user_id str
    @param token str
    @return user JSON object
"""
def update_user_token(db: Session, user_id: str, token: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.access_token = token
    db.commit()
    db.refresh(user)
    return user


"""
    Get User Token
    Get the user access_token from the db w.r.t. the userId.
    @urlParam user_id required The id of a users Example: uuid
    @urlParam db required for session
    @responseFile responses/users/get_user_token.json
    @response 400 {
    "errors": [
        "User not found."
      ]
     }
    @param user_data dict
    @param db mix
    @return string access_token
"""
def get_user_token(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.access_token

def get_users(db: Session):
    return db.query(models.User).options(joinedload(models.User.agents)).all()

def get_user(db: Session, user_id: UUID):
    return db.query(models.User).options(joinedload(models.User.agents)).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
