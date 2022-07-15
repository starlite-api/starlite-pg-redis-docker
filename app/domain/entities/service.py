from uuid import UUID

from starlite import Dependency, Parameter

from app import core

from . import schema
from .repository import Repository


class Service(core.Service[Repository, schema.Entity]):
    """
    Read only service for the root `entity` domain. CRUD operations must be performed through a
    provider's subdomain.
    """

    repository_type = Repository
    schema_type = schema.Entity

    @classmethod
    async def new(
        cls,
        *,
        entity_id: UUID | None = Parameter(),
        filters: core.dependencies.Filters = Dependency(),
    ) -> "Service":
        """
        Creates a new service object.

        Parameters
        ----------
        entity_id : UUID | None
            If not `None` filters database queries by id.
        filters : core.dependencies.Filters
            Passed through to repository on instantiation and used to filter the query.

        Returns
        -------
        Service
        """
        return cls(id_=entity_id, filters=filters)
