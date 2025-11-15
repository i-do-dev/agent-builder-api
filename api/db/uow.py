from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.session import async_session
from api.db.repositories.user import UserRepository

class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        # expose repos
        self.users = UserRepository(session)
        # self.agents = AgentRepository(session)
        # self.topics = TopicRepository(session) ...
        # self.actions = ActionRepository(session) ...

    async def commit(self): await self.session.commit()
    async def rollback(self): await self.session.rollback()

@asynccontextmanager
async def uow_context():
    async with async_session() as session:
        uow = UnitOfWork(session)
        try:
            yield uow
            await uow.commit()
        except Exception:
            await uow.rollback()
            raise
