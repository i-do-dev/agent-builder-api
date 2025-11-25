from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class Token(BaseModel):
    """ Access token  contract """
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """ Payload data contained in the token contract """
    sub: str
    exp: int
