from abc import ABC, abstractmethod
from pwdlib import PasswordHash

class IPasswordHasher(ABC):
    """Domain service interface for password hashing"""
    
    @abstractmethod
    def hash(self, plain_password: str) -> str:
        pass
    
    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        pass

class PasswordHasher(IPasswordHasher):
    """Concrete implementation using pwdlib"""
    
    def __init__(self):
        self._hasher = PasswordHash.recommended()
    
    def hash(self, plain_password: str) -> str:
        """Hash a plain password securely"""
        return self._hasher.hash(plain_password)
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self._hasher.verify(plain_password, hashed_password)