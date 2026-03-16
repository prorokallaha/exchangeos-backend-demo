from __future__ import annotations

import uuid

from app.db.models.organization_setting import OrganizationSetting
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.organization_setting import (
    OrganizationSettingCreate,
    OrganizationSettingUpdate,
)


class OrganizationSettingRepository(BaseRepository):
    @property
    def model(self) -> type[OrganizationSetting]:
        return OrganizationSetting

    async def get_by_key(self, organization_id: uuid.UUID, key: str) -> OrganizationSetting | None:
        return await self._crud.select(
            OrganizationSetting.organization_id == organization_id,
            OrganizationSetting.key == key,
        )

    async def list_by_org(self, organization_id: uuid.UUID) -> list[OrganizationSetting]:
        return list(await self._crud.select_many(OrganizationSetting.organization_id == organization_id))

    async def create(self, data: OrganizationSettingCreate) -> OrganizationSetting | None:
        return await self._crud.insert(**data)

    async def update(self, setting_id: uuid.UUID, data: OrganizationSettingUpdate) -> OrganizationSetting | None:
        rows = await self._crud.update(OrganizationSetting.id == setting_id, **data)
        return rows[0] if rows else None