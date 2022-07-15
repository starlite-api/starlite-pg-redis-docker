from typing import Any, Optional
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, text
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.model import InProviderDomain

from .types import EntitiesEnum


class Entity(InProviderDomain):
    name: Mapped[str]
    type: Mapped[EntitiesEnum] = mapped_column(Enum(EntitiesEnum, create_constraint=False))
    owner_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("entity.id"), index=True)
    extra: Mapped[dict[str, Any]] = mapped_column(pg.JSONB, server_default=text("'{}'::jsonb"))
    # ryno id is an implementation detail, not to be exposed to clients.
    ryno_id: Mapped[Optional[int]] = mapped_column(index=True)
