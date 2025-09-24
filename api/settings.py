from pydantic import AnyUrl, field_validator
from pydantic_settings import BaseSettings
from api.constants import NEO4J_ALLOWED_SCHEMES, NEO4J_INVALID_SCHEME_ERROR

class Settings(BaseSettings):
    app_name: str
    database_username: str
    database_password: str
    database_hostname: str
    database_port: int
    database_name: str
    neo4j_uri: AnyUrl
    neo4j_username: str
    neo4j_password: str

    @field_validator("neo4j_uri")
    @classmethod
    def validate_neo4j_scheme(cls, v):
        if v.scheme not in NEO4J_ALLOWED_SCHEMES:
            raise ValueError(NEO4J_INVALID_SCHEME_ERROR)
        return v
