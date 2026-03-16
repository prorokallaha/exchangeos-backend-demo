from __future__ import annotations

import uuid

from app.db.models.permission import Permission
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.permission import PermissionCreate, PermissionUpdate


class PermissionRepository(BaseRepository):
    @property
    def model(self) -> type[Permission]:
        return Permission

    async def get_by_id(self, permission_id: uuid.UUID) -> Permission | None:
        return await self._crud.select(Permission.id == permission_id)

    async def get_by_code(self, code: str) -> Permission | None:
        return await self._crud.select(Permission.code == code)

    async def list_all(self) -> list[Permission]:
        return list(await self._crud.select_many())

    async def list_by_ids(self, ids: list):
        if not ids:
            return []
        return await self._crud.select_many(
            self.model.id.in_(ids),
        )

    async def create(self, data: PermissionCreate) -> Permission | None:
        return await self._crud.insert(**data)

    async def update(self, permission_id: uuid.UUID, data: PermissionUpdate) -> Permission | None:
        rows = await self._crud.update(Permission.id == permission_id, **data)
        return rows[0] if rows else None