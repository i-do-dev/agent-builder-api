# api/db/session.py
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api.settings import Settings   

settings = Settings()
ASYNC_DSN = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"  # e.g. "postgresql+asyncpg://user:pass@host/db"

async_engine: AsyncEngine = create_async_engine(ASYNC_DSN, pool_pre_ping=True)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
