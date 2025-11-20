from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL
    database_username: str    
    database_password: str 
    database_hostname: str
    database_port: str    
    database_name: str

    # Neo4j
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str

    class Config:
        env_file = ".env"

settings = Settings()
