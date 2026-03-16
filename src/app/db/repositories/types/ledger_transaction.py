from __future__ import annotations

from typing import NotRequired, TypedDict
import uuid

from app.db.models.enums import LedgerTxStatus, LedgerTxType


class LedgerTransactionCreate(TypedDict):
    organization_id: uuid.UUID
    type: LedgerTxType
    status: LedgerTxStatus
    created_by_member_id: NotRequired[uuid.UUID | None]


class LedgerTransactionUpdate(TypedDict, total=False):
    status: NotRequired[LedgerTxStatus]