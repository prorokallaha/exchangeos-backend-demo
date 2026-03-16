from __future__ import annotations

import uuid

from app.db.models.order import Order
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.order import OrderCreate, OrderUpdate


class OrderRepository(BaseRepository):
    @property
    def model(self) -> type[Order]:
        return Order

    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        return await self._crud.select(Order.id == order_id)

    async def list_by_org(self, organization_id: uuid.UUID) -> list[Order]:
        return list(await self._crud.select_many(Order.organization_id == organization_id))

    async def list_by_assignee(self, organization_id: uuid.UUID, member_id: uuid.UUID) -> list[Order]:
        return list(
            await self._crud.select_many(
                Order.organization_id == organization_id,
                Order.assigned_to_member_id == member_id,
            )
        )

    async def list_by_creator(self, member_id: uuid.UUID) -> list[Order]:
        return list(
            await self._crud.select_many(
                self.model.created_by_member_id == member_id,
            )
        )

    async def create(self, data: OrderCreate) -> Order | None:
        return await self._crud.insert(**data)

    async def update(self, order_id: uuid.UUID, data: OrderUpdate) -> Order | None:
        rows = await self._crud.update(Order.id == order_id, **data)
        return rows[0] if rows else None