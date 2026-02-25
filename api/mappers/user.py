from src.core.entities.user import User, SecureUser
from api.contracts.requests.user import UserSignUpRequest
from api.contracts.responses.user import UserProfileResponse, UserSignUpResponse
from src.core.services.password_hasher import IPasswordHasher
from src.core.value_objects.password import PlainPassword

class UserMapper:
    """User mapper to convert between Model, Entity, and Response"""
     
    @staticmethod
    def signup_request_to_entity(request: UserSignUpRequest, password_hasher: IPasswordHasher) -> SecureUser:
        fields_mapping = {
            'username': request.username,
            'email': request.email,
            'first_name': request.first_name,
            'last_name': request.last_name
        }
        
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        """Create domain entity from signup request."""
        secure_user = SecureUser(**kwargs)
        secure_user.set_password(PlainPassword(request.password), password_hasher)
        return secure_user
    
    @staticmethod
    def entity_to_signup_response(entity: User) -> UserSignUpResponse:
        """Convert domain entity to UserSignUpResponse."""
        fields_mapping = {
            'username': entity.username,
            'email': entity.email,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'joined_at': entity.created_at.strftime("%m/%d/%Y %I:%M:%S %p") if entity.created_at else None
        }
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        return UserSignUpResponse(**kwargs)
    
    @staticmethod
    def entity_to_profile_response(entity: User) -> UserProfileResponse:
        """Convert domain entity to UserProfileResponse."""
        fields_mapping = {
            'username': entity.username,
            'email': entity.email,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'joined_at': entity.created_at.strftime("%m/%d/%Y %I:%M:%S %p") if entity.created_at else None
        }
        kwargs = {k: v for k, v in fields_mapping.items() if v is not None}
        return UserProfileResponse(**kwargs)
    
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