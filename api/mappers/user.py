from typing import Optional
from pydantic import BaseModel, ConfigDict
from api.db.models import User as UserModel
from api.entities.user import UserEntity, AuthUserEntity
from api.contracts.requests.user import UserSignUpRequest
from api.contracts.responses.user import UserSignUpResponse
from api.contracts.user import UserAuth, UserDataWithPassword, UserProfile
from datetime import datetime
from uuid import UUID

from api.services.password_hasher import IPasswordHasher
from api.value_objects.password import PlainPassword

class UserMapper:
    """User mapper to convert between Model, Entity, and Response"""
    
    @staticmethod
    def model_to_entity(model: UserModel) -> Optional[UserEntity]:
        """Convert Model to domain entity"""
        if not model:
            return None
            
        # Parse and validate the SQLAlchemy model using Pydantic
        class UserFromModel(BaseModel):
            """Pydantic model for User from SQLAlchemy model"""
            model_config = ConfigDict(from_attributes=True)

            id: UUID
            username: str
            email: str
            first_name: Optional[str]
            last_name: Optional[str]
            created_at: datetime
            
        user = UserFromModel.model_validate(model)
        
        # Convert to domain entity
        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at
        )
    
    @staticmethod
    def entity_to_model(entity: UserEntity) -> UserModel:
        # Convert domain entity to SQLAlchemy model
        fields_mapping = {
            'username': entity.username,
            'email': entity.email,
            'first_name': entity.first_name,
            'last_name': entity.last_name
        }

        # incorporate id and created_at if present
        if entity.id is not None:
            fields_mapping['id'] = entity.id

        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        return UserModel(**kwargs)

    @staticmethod
    def entity_to_model_with_password(entity: AuthUserEntity) -> UserModel:
        # Convert domain entity to SQLAlchemy model with password
        fields_mapping = {
            'username': entity.username,
            'email': entity.email,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'password': entity.password
        }

        if entity.id is not None:
            fields_mapping['id'] = entity.id
        
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        return UserModel(**kwargs)
    
    @staticmethod
    def entity_to_profile(entity: UserEntity) -> UserProfile:
        """Convert domain entity to UserProfile."""
        return UserProfile(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            created_at=entity.created_at,
        )
    
    @staticmethod
    def signup_request_to_entity(request: UserSignUpRequest, password_hasher: IPasswordHasher) -> AuthUserEntity:
        fields_mapping = {
            'username': request.username,
            'email': request.email,
            'first_name': request.first_name,
            'last_name': request.last_name
        }
        
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        """Create domain entity from signup request."""
        auth_user_entity = AuthUserEntity(**kwargs)
        auth_user_entity.set_password(PlainPassword(request.password), password_hasher)
        return auth_user_entity
    
    @staticmethod
    def entity_to_signup_response(entity: UserEntity) -> UserSignUpResponse:
        """Convert domain entity to UserSignUpResponse."""
        fields_mapping = {
            'id': entity.id,
            'username': entity.username,
            'email': entity.email,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'created_at': entity.created_at.strftime("%m/%d/%Y %I:%M:%S %p") if entity.created_at else None
        }
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        return UserSignUpResponse(**kwargs)
    
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