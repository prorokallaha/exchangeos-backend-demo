from __future__ import annotations

import uuid

from app.db.models.organization_member import OrganizationMember
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.member import MemberCreate, MemberUpdate


class OrganizationMemberRepository(BaseRepository):
    @property
    def model(self) -> type[OrganizationMember]:
        return OrganizationMember

    async def get_by_id(self, member_id: uuid.UUID) -> OrganizationMember | None:
        return await self._crud.select(self.model.id == member_id)

    async def get_by_org_and_user(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> OrganizationMember | None:
        return await self._crud.select(
            self.model.organization_id == organization_id,
            self.model.user_id == user_id,
        )

    async def list_by_org(self, organization_id: uuid.UUID) -> list[OrganizationMember]:
        return list(
            await self._crud.select_many(
                self.model.organization_id == organization_id,
            )
        )

    async def list_by_user(self, user_id: uuid.UUID) -> list[OrganizationMember]:
        return list(
            await self._crud.select_many(
                self.model.user_id == user_id,
            )
        )

    async def create(self, data: MemberCreate) -> OrganizationMember | None:
        return await self._crud.insert(**data)

    async def update(
        self,
        member_id: uuid.UUID,
        data: MemberUpdate,
    ) -> OrganizationMember | None:
        rows = await self._crud.update(self.model.id == member_id, **data)
        return rows[0] if rows else None