from __future__ import annotations
from typing import Generic, TypeVar, Protocol, Sequence, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
import uuid

T = TypeVar("T")

class RepositoryType(Protocol, Generic[T]):
    """ Interface for a generic repository pattern. """
    async def get(self, id: uuid.UUID) -> Optional[T]: ...
    async def add(self, obj: T) -> T: ...
    async def delete(self, obj: T) -> None: ...
    async def list(self, *, offset: int = 0, limit: int = 50, **filters: Any) -> Sequence[T]: ...
    async def update(self, id: uuid.UUID, values: dict[str, Any]) -> Optional[T]: ...
    async def update_where(self, values: dict[str, Any], **filters: Any) -> int: ...
    async def count(self, **filters: Any) -> int: ...
    async def get_by(self, **filters: Any) -> Optional[T]: ...


class Repository(Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: Any) -> Optional[T]:
        return await self.session.get(self.model, id)
    
    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush([obj])
        return obj
    
    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.flush([obj])

    async def list(self, *, offset: int = 0, limit: int = 50, **filters: Any) -> Sequence[T]:
        statement = select(self.model)
        for key, value in filters.items():
            if value is None:
                continue
            column = getattr(self.model, key, None)
            if column is None:
                continue
            statement = statement.where(column == value)

        statement = statement.offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())
    
    async def update(self, id: uuid.UUID, values: dict[str, Any]) -> Optional[T]:
        obj = await self.get(id)
        if not obj:
            return None
        for key, value in values.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        await self.session.flush([obj])
        # Optionally refresh to pull server defaults / triggers
        # await self.session.refresh(obj)
        return obj
    
    async def update_where(self, values: dict[str, Any], **filters: Any) -> int:
        statement = update(self.model).values(**values)
        for key, value in filters.items():
            if value is None:
                continue
            column = getattr(self.model, key, None)
            if column is None:
                continue
            statement = statement.where(column == value)
        
        result = await self.session.execute(statement)
        await self.session.flush()
        return result.rowcount or 0
    
    async def count(self, **filters: Any) -> int:
        statement = select(func.count()).select_from(self.model)
        for key, value in filters.items():
            if value is None:
                continue
            column = getattr(self.model, key, None)
            if column is None:
                continue
            statement = statement.where(column == value)
        
        result = await self.session.execute(statement)
        return result.scalar_one() or 0
    
    async def get_by(self, **filters: Any) -> Optional[T]:
        statement = select(self.model)
        for key, value in filters.items():
            if value is None:
                continue
            column = getattr(self.model, key, None)
            if column is None:
                continue
            statement = statement.where(column == value)
        
        result = await self.session.execute(statement)
        return result.scalars().first()