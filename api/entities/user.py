from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class User:
    """User domain entity representing the core business object"""
    id: uuid.UUID | None = field(default_factory=None)
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    created_at: datetime | None = field(default_factory=None)
    is_active: bool = True
    
    def get_full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()
    
    def can_authenticate(self) -> bool:
        """Check if user can authenticate"""
        return self.is_active
    
    def update_profile(self, first_name: str = None, last_name: str = None) -> None:
        """Update user profile information"""
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name

@dataclass
class UserWithPassword(User):
    """User entity with password for authentication scenarios"""
    password: str
    
    def has_valid_credentials(self, password_verifier) -> bool:
        """Check if user has valid credentials for authentication"""
        return self.is_active and password_verifier is not None