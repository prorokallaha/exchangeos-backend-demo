from __future__ import annotations

import uuid

from app.db.models.ledger_entry import LedgerEntry
from app.db.repositories.base import BaseRepository
from app.db.repositories.types.ledger_entry import LedgerEntryCreate


class LedgerEntryRepository(BaseRepository):
    @property
    def model(self) -> type[LedgerEntry]:
        return LedgerEntry

    async def list_by_transaction(self, transaction_id: uuid.UUID) -> list[LedgerEntry]:
        return list(await self._crud.select_many(LedgerEntry.transaction_id == transaction_id))

    async def create(self, data: LedgerEntryCreate) -> LedgerEntry | None:
        return await self._crud.insert(**data)