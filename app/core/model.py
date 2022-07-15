import re
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import MetaData
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.decl_api import declared_attr

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
meta = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    """
    Base for all SQLAlchemy declarative models.
    """

    __name__: str

    metadata = meta
    table_name_pattern = re.compile(r"(?<!^)(?=[A-Z])")
    type_annotation_map = {UUID: pg.UUID}

    # noinspection PyMethodParameters
    @declared_attr  # type:ignore[arg-type]
    def __tablename__(cls) -> str:  # type:ignore[override]  # pylint: disable=no-self-argument
        return re.sub(cls.table_name_pattern, "_", cls.__name__).lower()

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    created_date: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_date: Mapped[datetime] = mapped_column(default=datetime.now)
