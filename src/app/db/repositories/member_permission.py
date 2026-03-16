from __future__ import annotations

import uuid

from app.db.models.member_permission import MemberPermission
from app.db.repositories.base import BaseRepository


class MemberPermissionRepository(BaseRepository):
    @property
    def model(self) -> type[MemberPermission]:
        return MemberPermission

    async def list_by_member(self, member_id: uuid.UUID) -> list[MemberPermission]:
        return list(
            await self._crud.select_many(
                self.model.member_id == member_id,
            )
        )