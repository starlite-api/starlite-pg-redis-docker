from uuid import UUID

from starlite import Dependency, Parameter

from app import core
from app.domain import integrations
from app.domain.integrations import schema, types


class Service(core.Service[integrations.Repository, schema.Integration]):
    repository_type = integrations.Repository
    schema_type = schema.Integration

    @classmethod
    async def new(
        cls,
        *,
        provider_id: UUID = Parameter(),
        integration_type: types.IntegrationEnum | None = Parameter(),
        filters: core.dependencies.Filters = Dependency(),
    ) -> "Service":
        """
        Creates a new service object.

        Parameters
        ----------
        provider_id : UUID | None
            ID of provider that provides the integration.
        integration_type : types.IntegrationEnum | None
            Filters the query by integration type if not `None`
        filters : core.dependencies.Filters
            Passed through to repository on instantiation and used to filter the query.

        Returns
        -------
        Service
        """
        inst = cls(id_=None, filters=filters)
        inst.repository.filter_select_by_kwargs(provider_id=provider_id)
        if integration_type is not None:
            inst.repository.filter_select_by_kwargs(type=integration_type)
        return inst
