from api.db.uow import UnitOfWork, uow_context
from typing import AsyncGenerator
from typing import Annotated
from fastapi import Depends

# Unit of Work dependency to perform DB operations within a transaction
async def get_db() -> AsyncGenerator[UnitOfWork, None]:
    async with uow_context() as uow:
        yield uow

# Create a type alias for easier usage in FastAPI dependencies
Db = Annotated[UnitOfWork, Depends(get_db)]