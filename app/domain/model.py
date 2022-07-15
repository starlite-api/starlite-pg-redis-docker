from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app import core


class InProviderDomain(core.Base):
    __abstract__ = True

    provider_id: Mapped[UUID] = mapped_column(ForeignKey("provider.id"), nullable=False)
