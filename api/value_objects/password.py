from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Self

if TYPE_CHECKING:
    from api.services.password_hasher import IPasswordHasher

@dataclass(frozen=True)
class HashedPassword:
    """Value object representing a hashed password"""
    value: Optional[str] = field(default=None)
    
    @classmethod
    def from_plain(cls, plain_password: str, hasher: 'IPasswordHasher') -> Self:
        """Create hashed password from plain text"""
        if not plain_password or len(plain_password) < 8:
            raise ValueError("Password too weak")
        
        hashed = hasher.hash(plain_password)
        return cls(hashed)
    
    def verify_against(self, plain_password: str, hasher: 'IPasswordHasher') -> bool:
        """Verify plain password against this hash"""
        return hasher.verify(plain_password, self.value)

@dataclass(frozen=True)
class PlainPassword:
    """Value object for plain text password with validation"""
    value: str
    
    def hash_with(self, hasher: 'IPasswordHasher') -> HashedPassword:
        """Convert to hashed password"""
        return HashedPassword.from_plain(self.value, hasher)