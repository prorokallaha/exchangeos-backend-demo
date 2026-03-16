from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.db.models.enums import EntryDirection, LedgerTxStatus, LedgerTxType


class LedgerTransactionOut(BaseModel):
    id: UUID
    organization_id: UUID
    type: LedgerTxType
    status: LedgerTxStatus
    created_by_member_id: UUID | None


class LedgerEntryOut(BaseModel):
    id: UUID
    organization_id: UUID
    transaction_id: UUID
    account_id: UUID
    direction: EntryDirection
    amount: Decimal
    currency: str
    description: str | None