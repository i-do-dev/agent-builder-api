from __future__ import annotations
from typing import Generic, TypeVar, Protocol, Sequence, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from uuid import UUID

T = TypeVar("T")
M = TypeVar("M")

class RepositoryType(Protocol, Generic[T, M]):
    """ Interface for a generic repository pattern. """
    async def get_model(self, id: UUID) -> Optional[M]: ...
    async def get(self, id: UUID) -> Optional[T]: ...
    async def add_model(self, obj: M) -> M: ...
    async def add(self, obj: T) -> T: ...
    async def delete(self, obj: T) -> None: ...
    async def list(self, *, offset: int = 0, limit: int = 50, **filters: Any) -> Sequence[T]: ...
    async def update(self, id: UUID, values: dict[str, Any]) -> Optional[T]: ...
    async def update_where(self, values: dict[str, Any], **filters: Any) -> int: ...
    async def count(self, **filters: Any) -> int: ...
    async def get_by(self, **filters: Any) -> Optional[T]: ...


class Repository(Generic[T, M]):
    model: type[M]

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_model(self, id: UUID) -> Optional[M]:
        return await self.session.get(self.model, id)

    async def get(self, id: UUID) -> Optional[T]:
        model: M = await self.get_model(id)
        if model is None:
            return None
        return await self._model_to_entity(model)
    
    # Abstract methods for mapping (implemented in concrete repositories)
    async def _model_to_entity(self, model: M) -> T:
        """Convert ORM model to domain entity - implement in subclass"""
        raise NotImplementedError("Subclass must implement _model_to_entity")

    async def add(self, obj: T) -> T:
        model: M = await self._entity_to_model(obj)
        added_model = await self.add_model(model)
        return await self._model_to_entity(added_model)
    
    async def add_model(self, obj: M) -> M:
        self.session.add(obj)
        await self.session.flush([obj])
        return obj
    
    async def _entity_to_model(self, entity: T) -> M:
        """Convert domain entity to ORM model - implement in subclass"""
        raise NotImplementedError("Subclass must implement _entity_to_model")
    

    async def delete(self, obj: T) -> None:
        id = getattr(obj, 'id', None)
        if id is None:
            raise ValueError("Model Object must have an 'id' attribute to delete")
        model = await self.get_model(id)
        if model is None:
            raise ValueError(f"No model found with id {id} to delete")
        await self.session.delete(model)
        await self.session.flush()

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
        # return list(result.scalars().all())
        models = result.scalars().all()
        return [await self._model_to_entity(model) for model in models]
    
    async def update(self, id: UUID, values: dict[str, Any]) -> Optional[T]:
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
        obj = result.scalars().first()
        if obj is None:
            return None
        return await self._model_to_entity(obj)