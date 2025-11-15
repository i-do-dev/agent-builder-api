from api.db.uow import UnitOfWork, uow_context
from typing import AsyncGenerator

# Unit of Work dependency to perform DB operations within a transaction
async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with uow_context() as uow:
        yield uow
