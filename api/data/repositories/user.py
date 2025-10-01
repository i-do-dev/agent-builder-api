from typing import Optional
from api.data.repositories.base import Repository
from api.data.models import User

class UserRepository(Repository[User]):
    """Repository for User model."""
    model = User

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email."""
        return await self.get_by(email=email)
