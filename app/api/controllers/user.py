from pydantic import UUID4
from starlite import Controller, Provide, delete, get, post, put

from app.constants import USER_CONTROLLER_PATH
from app.models import UserCreateDTO, UserReadDTO
from app.repositories import UserRepository
from app.utils import get_password_hash


class UserController(Controller):
    path = USER_CONTROLLER_PATH

    dependencies = {"user_repository": Provide(UserRepository)}

    @post()
    async def create_user(self, data: UserCreateDTO, user_repository: UserRepository) -> UserReadDTO | None:
        return await user_repository.create(data=data)

    @get()
    async def list_users(self, user_repository: UserRepository, offset: int = 0, limit: int = 100) -> list[UserReadDTO]:
        return await user_repository.get_many(offset=offset, limit=limit)

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4, user_repository: UserRepository) -> UserReadDTO | None:
        return await user_repository.get_one(instance_id=user_id)

    @put(path="/{user_id:uuid}")
    async def update_user(
        self, user_id: UUID4, data: UserCreateDTO, user_repository: UserRepository
    ) -> UserReadDTO | None:
        return await user_repository.partial_update(instance_id=user_id, data=data)

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4, user_repository: UserRepository) -> UserReadDTO | None:
        return await user_repository.delete(instance_id=user_id)
