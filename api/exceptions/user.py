# api/infrastructure/exceptions/user_exceptions.py
class UserError(Exception):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserError):
    """Raised when a user is not found"""
    def __init__(self, identifier: str = None):
        self.identifier = identifier
        message = f"User not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message)

class UserAlreadyExistsError(UserError):
    """Raised when trying to create a user that already exists"""
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"User with {field} '{value}' already exists")

class UserValidationError(UserError):
    """Raised when user data validation fails"""
    pass

class UserAuthenticationError(UserError):
    """Raised when user authentication fails"""
    pass