from __future__ import annotations

import uuid

from app.db.models.ledger_transaction import LedgerTransaction
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.ledger_transaction import (
    LedgerTransactionCreate,
    LedgerTransactionUpdate,
)


class LedgerTransactionRepository(BaseRepository):
    @property
    def model(self) -> type[LedgerTransaction]:
        return LedgerTransaction

    async def get_by_id(self, tx_id: uuid.UUID) -> LedgerTransaction | None:
        return await self._crud.select(LedgerTransaction.id == tx_id)

    async def list_by_org(self, organization_id: uuid.UUID) -> list[LedgerTransaction]:
        return list(await self._crud.select_many(LedgerTransaction.organization_id == organization_id))

    async def create(self, data: LedgerTransactionCreate) -> LedgerTransaction | None:
        return await self._crud.insert(**data)

    async def update(self, tx_id: uuid.UUID, data: LedgerTransactionUpdate) -> LedgerTransaction | None:
        rows = await self._crud.update(LedgerTransaction.id == tx_id, **data)
        return rows[0] if rows else None