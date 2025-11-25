from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from typing import Optional
from api.db.repositories.base import Repository
from api.db.models import User

class UserRepository(Repository[User]):
    """Repository for User model."""
    model = User

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by their username."""
        return await self.get_by(username=username)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email."""
        return await self.get_by(email=email)
    
    async def get_valid(self, username_or_email) -> Optional[User]:
        statement = select(self.model).where(
            or_(
                self.model.username == username_or_email, self.model.email == username_or_email                
            )
        )
        result = await self.session.execute(statement)
        return result.scalars().first()
    
    async def get_with_agents(self, user_id: str) -> Optional[User]:
        """Get user with agents - matches model_to_entity_with_agents"""
        statement = select(self.model).options(
            selectinload(self.model.agents)
        ).where(self.model.id == user_id)
        
        result = await self.session.execute(statement)
        return result.scalars().first()