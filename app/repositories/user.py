from typing import cast

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User, UserCreateDTO
from app.utils.security import get_password_hash, verify_password

from ..exceptions import RepositoryException
from .base import AbstractBaseRepository


class UserRepository(AbstractBaseRepository[User]):
    model = User

    @classmethod
    async def create(cls, data: UserCreateDTO) -> User | None:
        try:
            data = data.dict()
            data.update(hashed_password=get_password_hash(data["password"]))
            return await super().create(data=data)
        except (TypeError, ValueError) as e:
            raise RepositoryException from e

    @classmethod
    async def get_by_username(cls, username: str) -> User | None:
        try:
            async with cls.session_maker() as async_session:
                results = await async_session.execute(select(User).where(User.username == username))
                return cast(User | None, results.first())
        except SQLAlchemyError as e:
            raise RepositoryException("unable to retrieve user") from e

    @classmethod
    async def authenticate(cls, username: str, password: str) -> User | None:  # todo remove hashed_pass
        user = await cls.get_by_username(username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
