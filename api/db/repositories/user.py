from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import Optional
from api.db.repositories.base import Repository
from api.db.models import User as UserModel
from api.entities.user import User as UserEntity, UserWithPassword
from api.mappers.user import UserMapper

class UserRepository(Repository[UserEntity, UserModel]):
    """Repository for User model."""
    model = UserModel

    async def _model_to_entity(self, model: UserModel) -> UserEntity:
        """Convert UserModel to User entity."""
        return UserMapper.model_to_entity(model)
    
    async def _entity_to_model(self, entity: UserEntity) -> UserModel:
        return UserMapper.entity_to_model_with_password(entity)

    async def add(self, entity: UserWithPassword) -> Optional[UserEntity]:
        # call parent add method
        return await super().add(entity)

    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        """Get a user by their username."""
        return await self.get_by(username=username)
    
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get a user by their email."""
        return await self.get_by(email=email)
    
    async def get_valid(self, username_or_email) -> Optional[UserEntity]:
        statement = select(self.model).where(
            or_(
                self.model.username == username_or_email, self.model.email == username_or_email                
            )
        )
        result = await self.session.execute(statement)
        obj = result.scalars().first()
        if obj is None:
            return None
        return self._model_to_entity(obj)    

    # async def get_with_agents(self, user_id: str) -> Optional[User]:
    #     """Get user with agents - matches model_to_entity_with_agents"""
    #     statement = select(self.model).options(
    #         selectinload(self.model.agents)
    #     ).where(self.model.id == user_id)
        
    #     result = await self.session.execute(statement)
    #     return result.scalars().first()
    