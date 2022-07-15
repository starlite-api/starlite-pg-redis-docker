from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.model import InProviderDomain

from . import types


class Integration(InProviderDomain):
    type: Mapped[types.IntegrationEnum] = mapped_column(Enum(types.IntegrationEnum), index=True)
    __table_args__ = (UniqueConstraint("provider_id", "type", name="ux_integration_provider_type"),)
