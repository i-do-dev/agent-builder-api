from typing import Optional
from pydantic import BaseModel, ConfigDict
from api.contracts.requests.user import UserSignUpRequest
from api.db.models import User as UserModel
from api.entities.user import User, UserWithPassword
from api.contracts.responses.user import UserResponse

class UserMapper:
    """User mapper to convert between Model, Entity, and Response"""
    
    @staticmethod
    def model_to_entity(model: UserModel) -> Optional[User]:
        """Convert Model to domain entity"""
        if not model:
            return None
            
        # Parse and validate the SQLAlchemy model using Pydantic
        class UserFromModel(BaseModel):
            """Pydantic model for User from SQLAlchemy model"""
            model_config = ConfigDict(from_attributes=True)

            id: str
            username: str
            email: str
            first_name: Optional[str]
            last_name: Optional[str]
            created_at: str
            disabled: bool
            
        user = UserFromModel.model_validate(model)
        
        # Convert to domain entity
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
            is_active=not user.disabled
        )
     
    @staticmethod
    def entity_to_response(entity: User) -> UserResponse:
        #Convert entity to response using Pydantic
        return UserResponse(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            full_name=entity.get_full_name(),
            created_at=entity.created_at,
            is_active=entity.is_active
        )
    
    @staticmethod
    def signup_request_to_entity(request: UserSignUpRequest, hashed_password: str) -> UserWithPassword:
        """Create domain entity from signup request."""
        return UserWithPassword(
            username=request.username,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            password=hashed_password,
        )
    
    """
    @staticmethod
    def model_to_entity_with_agents(model: UserModel) -> Optional[User]:
        #Explicit method for user + agents use case
        user_entity = UserMapper.model_to_entity_basic(model)
        
        if hasattr(model, 'agents') and model.agents:
            from api.mappers.agent import AgentMapper
            user_entity.agents = [
                AgentMapper.model_to_entity_basic(agent) 
                for agent in model.agents
            ]
        
        return user_entity
    
    @staticmethod
    def entity_to_response_with_agents(entity: User) -> UserWithAgentsResponse:
        #Explicit method for response with agents
        from api.mappers.agent import AgentMapper
        
        return UserWithAgentsResponse(
            # ... user fields ...
            agents=[
                AgentMapper.entity_to_response(agent) 
                for agent in getattr(entity, 'agents', [])
            ]
        )
    """