from __future__ import annotations

import uuid

from app.db.models.role import Role
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.role import RoleCreate, RoleUpdate


class RoleRepository(BaseRepository):
    @property
    def model(self) -> type[Role]:
        return Role

    async def get_by_id(self, role_id: uuid.UUID) -> Role | None:
        return await self._crud.select(Role.id == role_id)

    async def get_by_name(self, organization_id: uuid.UUID, name: str) -> Role | None:
        return await self._crud.select(
            Role.organization_id == organization_id,
            Role.name == name,
        )

    async def list_by_org(self, organization_id: uuid.UUID) -> list[Role]:
        return list(await self._crud.select_many(Role.organization_id == organization_id))

    async def create(self, data: RoleCreate) -> Role | None:
        return await self._crud.insert(**data)

    async def update(self, role_id: uuid.UUID, data: RoleUpdate) -> Role | None:
        rows = await self._crud.update(Role.id == role_id, **data)
        return rows[0] if rows else None