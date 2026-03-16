from __future__ import annotations

from app.db.models.organization import Organization
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.organization import OrganizationCreate, OrganizationUpdate


class OrganizationRepository(BaseRepository):
    @property
    def model(self) -> type[Organization]:
        return Organization

    async def get_by_id(self, org_id) -> Organization | None:
        return await self._crud.select(Organization.id == org_id)

    async def create(self, data: OrganizationCreate) -> Organization | None:
        return await self._crud.insert(**data)

    async def update(self, org_id, data: OrganizationUpdate) -> Organization | None:
        rows = await self._crud.update(Organization.id == org_id, **data)
        return rows[0] if rows else None