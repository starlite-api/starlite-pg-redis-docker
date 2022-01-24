from abc import ABC
from typing import Any, Generic, TypeVar, cast
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.state import database
from app.exceptions import RepositoryException
from app.models.base import Base

T = TypeVar("T", bound=Base)


class AbstractBaseRepository(ABC, Generic[T]):
    model: type[T]

    @staticmethod
    def session_maker() -> sessionmaker:
        engine = database
        return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @classmethod
    async def get_many(cls, *, offset: int = 0, limit: int = 100) -> list[T]:
        try:
            async with cls.session_maker() as async_session:
                results = await async_session.execute(select(cls.model).offset(offset).limit(limit))
                return cast(list[T], results.all())
        except SQLAlchemyError as e:
            raise RepositoryException("Unable to retrieve instances") from e

    @classmethod
    async def get_one(cls, instance_id: UUID) -> T | None:
        try:
            async with cls.session_maker() as async_session:
                results = await async_session.execute(select(cls.model).where(cls.model.id == instance_id))
                return cast(T | None, results.first())
        except SQLAlchemyError as e:
            raise RepositoryException("Unable to retrieve instance") from e

    @classmethod
    async def create(cls, data: BaseModel | dict[str, Any]) -> T | None:
        try:
            async with cls.session_maker() as async_session:
                async with async_session.begin():
                    if isinstance(data, BaseModel):
                        data = data.dict()
                    instance = cls.model(**data)
                    async_session.add(instance)
                    await async_session.commit()
                    await async_session.refresh(instance)
                    await async_session.dispose()
                    return cast(T, instance)
        except SQLAlchemyError as e:
            raise RepositoryException("Unable to create instance") from e

    @classmethod
    async def partial_update(cls, instance_id: UUID, data: BaseModel) -> T:
        try:
            async with cls.session_maker() as async_session:
                results = await async_session.execute(select(cls.model).where(cls.model.id == instance_id))
                instance = results.first()
                for key, value in data.dict().items():
                    setattr(instance, key, value)
                async_session.add(instance)
                await async_session.commit()
                await async_session.refresh(instance)
                return cast(T, instance)
        except SQLAlchemyError as e:
            raise RepositoryException("Unable to update instance") from e

    @classmethod
    async def delete(cls, instance_id: UUID) -> None:
        try:
            async with cls.session_maker() as async_session:
                results = await async_session.execute(select(cls.model).where(cls.model.id == instance_id))
                await async_session.delete(results)
                await async_session.commit()
        except SQLAlchemyError as e:
            raise RepositoryException("Unable to delete instance") from e
