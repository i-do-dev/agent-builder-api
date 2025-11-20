from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db_postgres import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError
from schemas import agent_schemas, topic_schemas, user_schemas
from crud import user_crud as user_crud
from crud import agent_crud as agent_crud
from crud import topic_crud as topic_crud
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_current_user, TOKEN_BLACKLIST
import os
import models

SECRET_KEY = os.getenv("JWT_SECRET", "fallback-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# NOTE: no prefix here — main.py mounts this router under /api
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# tokenUrl must match the mounted login route (app-level '/api/users/login')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# User signup endpoint
@router.post("/users/signup", response_model=user_schemas.UserResponse)
def signup(user: user_schemas.UserCreateRequest, db: Session = Depends(get_db)):
    existing = user_crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = user_crud.create_user(db, user)
    return created_user

# Validate user access token
@router.get("/users/validate-token")
def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "payload": payload}
    except JWTError:
        return {"valid": False}

# User login endpoint
@router.post("/users/login", response_model=user_schemas.TokenResponse)
def login_user(user_credentials: user_schemas.UserLogin, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, user_credentials.email)
    if not user or not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")    
    access_token = create_access_token({"sub": str(user.id)})
    user_crud.update_user_token(db, str(user.id), access_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_id": str(user.id)
    }


# Get list of all users (requires login)
@router.get("/users/", response_model=list[user_schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user: user_schemas.UserResponse = Depends(get_current_user)):
    return user_crud.get_users(db)

# Get single user by ID (requires login)
@router.get("/users/{user_id}", response_model=user_schemas.UserResponse)
def get_user_by_id(user_id: str, db: Session = Depends(get_db), current_user: user_schemas.UserResponse = Depends(get_current_user)):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"User {user_id} does not exist"
            }
        )
    return user

# Logout user and blacklist token
@router.post("/users/logout")
def logout_user(token: str = Depends(oauth2_scheme), current_user: user_schemas.UserResponse = Depends(get_current_user)):
    TOKEN_BLACKLIST.add(token)
    return {"message": "Logout successful. Token has been revoked."}

# Get the user token for an existing user session to verify user authentication and access rights.
@router.post("/users/get-user-token")
def get_user_token(user_data: dict, db: Session = Depends(get_db)):
    user_id = user_data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    token = user_crud.get_user_token(db, user_id)
    if not token:
        raise HTTPException(status_code=401, detail="No active token. Login again.")

    return {
        "valid": True,
        "access_token": token,
        "user_id": user_id
    }

"""
    Create Flow
    Handles flow creation by validating the user, ensuring or creating an agent,
    optionally creating a linked topic, and returning their details.
    @urlParam user-id required The id of the user making the request. Example: uuid
    @urlParam db required Database session instance.
    @responseFile responses/users/create_flow.json
    @response 400 {
        "errors": [
            "user-id and agent_name are required"
        ]
    }
    @response 403 {
        "errors": [
            "User ID in request does not match authenticated user."
        ]
    }
    @response 500 {
        "errors": [
            "Error creating agent.",
            "Error creating topic."
        ]
    }
    @param request_data dict The request body containing:
           - user-id (string) required
           - agent_name (string) required
           - topic_label (string) optional

    @param current_user mix Authenticated user object.
    @param db mix Database session instance.
    @return dict
"""
# Handles flow creation by validating user, ensuring/creating agent, optionally creating a linked topic, and returning their details.
@router.post("/create-flow")
def create_flow(
    request_data: dict,  # Raw dict to accept the specific format you described
    current_user: models.User = Depends(get_current_user), # Validates the token from header
    db: Session = Depends(get_db)  # This line was missing in your code
):
    # Extract required and optional data from the request body
    user_id_from_request = request_data.get("user-id")
    agent_name = request_data.get("agent_name")
    topic_label = request_data.get("topic_label") # Optional

    # Validation: Check if required fields are present
    if not user_id_from_request or not agent_name:
        raise HTTPException(status_code=400, detail="user-id and agent_name are required")

    # Optional: Validate that the user_id in the request matches the authenticated user
    # This is an extra security check. You can rely only on the token validation if you prefer.
    if str(current_user.id) != str(user_id_from_request):
         raise HTTPException(status_code=403, detail="User ID in request does not match authenticated user.")

    # Find the agent by name and user_id to ensure it belongs to the authenticated user
    # Check if an agent with the same name already exists for this user
    existing_agent = db.query(models.Agent).filter(
        models.Agent.name == agent_name,
        models.Agent.user_id == current_user.id
    ).first()

    if existing_agent:
        # If agent already exists, you can choose to link the topic to it or return an error
        # For now, let's assume creating a new topic for an existing agent is fine
        agent_to_use = existing_agent
        agent_created = False
    else:
        # Create a new agent if it doesn't exist
        agent_create_request = agent_schemas.AgentCreateRequest(name=agent_name)
        try:
            agent_to_use = agent_crud.create_agent(db, agent_create_request, current_user.id)
            agent_created = True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating agent: {str(e)}")

    # If topic_label is provided, check for existing topic and create if necessary
    created_or_found_topic = None
    if topic_label:
        # --- NEW LOGIC: Check if a topic with this label already exists for this specific agent ---
        existing_topic_for_agent = db.query(models.Topic).filter(
            models.Topic.label == topic_label,
            models.Topic.agent_id == agent_to_use.id # Link to the specific agent found/created above
        ).first()

        if existing_topic_for_agent:
            # If topic with this label already exists for the agent, use it
            created_or_found_topic = existing_topic_for_agent
            print(f"Topic '{topic_label}' already exists for agent '{agent_to_use.name}'. Using existing topic.")
        else:
            # If no existing topic found for this agent-topic_label pair, create a new one
            topic_create_request = topic_schemas.TopicCreateRequest(
                label=topic_label,
                agent_id=agent_to_use.id # Link to the agent found or created above
            )
            # Call CRUD function to create topic
            try:
                created_or_found_topic = topic_crud.create_topic(db, topic_create_request)
                print(f"Created new topic '{topic_label}' for agent '{agent_to_use.name}'.")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error creating topic: {str(e)}")
    else:
        # If no topic_label was provided, we don't create or find a topic
        print("No topic_label provided, skipping topic creation/linking.")

    # Return success response
    # Use 'created_or_found_topic' which will be the existing one or the newly created one
    return {
        "message": "Flow processed successfully",
        "user_id": str(current_user.id),
        "agent_id": str(agent_to_use.id),
        "topic_id": str(created_or_found_topic.id) if created_or_found_topic else None,
        "agent_name": agent_to_use.name,
        "topic_label": topic_label if created_or_found_topic else None,
        "agent_created": agent_created, # Indicate if a new agent was created
        "topic_found_or_created": "found" if (topic_label and created_or_found_topic and existing_topic_for_agent) else ("created" if (topic_label and created_or_found_topic and not existing_topic_for_agent) else "none") # Added status for topic
    }
