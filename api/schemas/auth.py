from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserProfile(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None

class UserAuth(UserProfile):
    password: str

class UserSignUpRequest(UserAuth):
    confirm_password: str
