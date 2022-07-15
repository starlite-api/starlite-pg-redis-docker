from sqlalchemy.orm import Mapped, mapped_column

from app.core.model import Base


class Provider(Base):
    name: Mapped[str] = mapped_column(unique=True)
