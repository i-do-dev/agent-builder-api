from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from api.value_objects.password import HashedPassword
from api.value_objects.password import PlainPassword

if TYPE_CHECKING:
    from api.services.password_hasher import IPasswordHasher

@dataclass
class User:
    """User domain entity representing the core business object"""
    id: Optional[UUID] = field(default=None)
    username: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    first_name: Optional[str] = field(default=None)
    last_name: Optional[str] = field(default=None)
    created_at: Optional[datetime] = field(default=None)
    is_active: bool = field(default=True)
    
    def get_full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

@dataclass
class SecureUser(User):
    """User entity with password for authentication scenarios"""
    password: Optional[HashedPassword] = field(default=None)

    def set_password(self, plain_password: PlainPassword, password_hasher: Optional["IPasswordHasher"]) -> None:
        """Set user's password by hashing the plain password"""
        if password_hasher is None:
            raise ValueError("Password hasher is not set")
        self.password = plain_password.hash_with(password_hasher)
    
    def authenticate(self, plain_password: PlainPassword, password_hasher: Optional["IPasswordHasher"]) -> bool:
        """Authenticate user by verifying the plain password against the stored hash"""
        if self.password is None or password_hasher is None:
            return False
        return self.password.verify_against(plain_password.value, password_hasher)