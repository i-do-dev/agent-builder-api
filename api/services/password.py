from pwdlib import PasswordHash

class PasswordService:
    """Service for handling password hashing and verification."""
    
    def __init__(self):
        self.password_hash = PasswordHash.recommended()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return self.password_hash.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a plain password."""
        return self.password_hash.hash(password)