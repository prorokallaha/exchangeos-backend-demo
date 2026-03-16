from __future__ import annotations

import uuid

from app.db.models.payment_requisite import PaymentRequisite
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.payment_requisite import (
    PaymentRequisiteCreate,
    PaymentRequisiteUpdate,
)


class PaymentRequisiteRepository(BaseRepository):
    @property
    def model(self) -> type[PaymentRequisite]:
        return PaymentRequisite

    async def get_by_id(self, requisite_id: uuid.UUID) -> PaymentRequisite | None:
        return await self._crud.select(self.model.id == requisite_id)

    async def list_by_org(self, organization_id: uuid.UUID) -> list[PaymentRequisite]:
        return list(
            await self._crud.select_many(
                self.model.organization_id == organization_id,
            )
        )

    async def create(self, data: PaymentRequisiteCreate) -> PaymentRequisite | None:
        return await self._crud.insert(**data)

    async def update(
        self,
        requisite_id: uuid.UUID,
        data: PaymentRequisiteUpdate,
    ) -> PaymentRequisite | None:
        rows = await self._crud.update(self.model.id == requisite_id, **data)
        return rows[0] if rows else None