from __future__ import annotations

from decimal import Decimal
from typing import TypedDict
import uuid

from app.db.models.enums import EntryDirection


class LedgerEntryCreate(TypedDict):
    organization_id: uuid.UUID
    transaction_id: uuid.UUID
    account_id: uuid.UUID
    direction: EntryDirection
    amount: Decimal
    currency: str
    description: str