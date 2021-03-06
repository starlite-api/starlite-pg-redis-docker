from typing import Generic, TypeVar
from uuid import UUID

from .dependencies import Filters
from .model import Base
from .repository import Repository
from .schema import Schema

T = TypeVar("T")
T_model = TypeVar("T_model", bound=Base)
T_repository = TypeVar("T_repository", bound=Repository)
T_schema = TypeVar("T_schema", bound=Schema)
T_service = TypeVar("T_service", bound="Service")


class Service(Generic[T_model, T_repository, T_schema]):
    model: type[T_model]
    repository_type: type[T_repository]
    schema: type[T_schema]

    def __init__(
        self,
        *,
        id_: UUID | None,
        filters: Filters,
    ) -> None:
        self.repository = self.repository_type(
            id_=id_,
            id_filter=filters.id,
            created_filter=filters.created,
            updated_filter=filters.updated,
            limit_offset=filters.limit_offset,
        )

    async def create(self, data: T_schema) -> T_schema:
        """
        Default create handler.

        Parameters
        ----------
        data : T_Schema

        Returns
        -------
        T_Schema
        """
        model = await self.repository.create(data.dict())
        return self.schema.from_orm(model)

    async def list(self) -> list[T_schema]:
        """
        Default list view handler.

        Returns
        -------
        list[T_Schema]
        """
        models: list[T_model] = await self.repository.scalars()  # type:ignore[assignment]
        return [self.schema.from_orm(i) for i in models]

    async def update(self, data: T_schema) -> T_schema:
        """
        Default update view handler.

        Parameters
        ----------
        data : T_Schema

        Returns
        -------
        T_Schema
        """
        model = self.repository.update(data.dict())
        return self.schema.from_orm(model)

    async def upsert(self, data: T_schema) -> T_schema:
        """
        Default upsert view handler.

        Parameters
        ----------
        data : T_Schema

        Returns
        -------
        T_Schema
        """
        model = await self.repository.upsert(data.dict())
        return self.schema.from_orm(model)

    async def show(self) -> T_schema:
        """
        Default member view handler.

        Returns
        -------
        T_Schema
        """
        model = await self.repository.scalar()
        return self.schema.from_orm(model)

    async def destroy(self) -> T_schema:
        """
        Default delete view handler.

        Returns
        -------
        T_Schema
        """
        model = self.repository.delete()
        return self.schema.from_orm(model)
