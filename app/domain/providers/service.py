from uuid import UUID

from starlite import Dependency, Parameter

from app import core

from . import model, schema
from .repository import Repository


class Service(core.Service[model.Provider, Repository, schema.Provider]):
    model = model.Provider
    repository_type = Repository
    schema = schema.Provider

    @classmethod
    async def new(
        cls,
        *,
        provider_id: UUID | None = Parameter(),
        filters: core.dependencies.Filters = Dependency(),
    ) -> "Service":
        """
        Creates a new service object.

        Parameters
        ----------
        provider_id : UUID | None
            If not `None` filters database queries by id.
        filters : core.dependencies.Filters
            Passed through to repository on instantiation and used to filter the query.

        Returns
        -------
        Service
        """
        return cls(id_=provider_id, filters=filters)
