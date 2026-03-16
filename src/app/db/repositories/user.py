from __future__ import annotations

from collections.abc import Sequence

from app.db.models.user import User
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.user import UserCreate, UserUpdate


class UserRepository(BaseRepository):
    @property
    def model(self) -> type[User]:
        return User

    async def get_by_id(self, user_id) -> User | None:
        return await self._crud.select(User.id == user_id)

    async def get_by_login(self, login: str) -> User | None:
        return await self._crud.select(User.login == login)

    async def get_many(self, *, offset: int = 0, limit: int = 100) -> Sequence[User]:
        return await self._crud.select_many(offset=offset, limit=limit)

    async def create(self, data: UserCreate) -> User | None:
        return await self._crud.insert(**data)

    async def update(self, user_id, data: UserUpdate) -> User | None:
        rows = await self._crud.update(User.id == user_id, **data)
        return rows[0] if rows else None