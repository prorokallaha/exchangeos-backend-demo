from __future__ import annotations

import uuid

from app.db.models.role_permission import RolePermission
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.role_permission import RolePermissionCreate


class RolePermissionRepository(BaseRepository):
    @property
    def model(self) -> type[RolePermission]:
        return RolePermission

    async def exists_link(self, role_id: uuid.UUID, permission_id: uuid.UUID) -> bool:
        return await self._crud.exists(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )

    async def list_by_role(self, role_id: uuid.UUID) -> list[RolePermission]:
        return list(await self._crud.select_many(RolePermission.role_id == role_id))

    async def create(self, data: RolePermissionCreate) -> RolePermission | None:
        return await self._crud.insert(**data)