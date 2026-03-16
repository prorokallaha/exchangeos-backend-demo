from __future__ import annotations

from decimal import Decimal
from typing import NotRequired, TypedDict
import uuid

from app.db.models.enums import OrderStatus, OrderType


class OrderCreate(TypedDict):
    organization_id: uuid.UUID
    type: OrderType
    status: OrderStatus
    amount_in: Decimal
    currency_in: str
    amount_out: Decimal
    currency_out: str
    rate: Decimal
    created_by_member_id: NotRequired[uuid.UUID | None]
    assigned_to_member_id: NotRequired[uuid.UUID | None]
    settlement_tx_id: NotRequired[uuid.UUID | None]
    meta: NotRequired[dict]


class OrderUpdate(TypedDict, total=False):
    status: NotRequired[OrderStatus]
    assigned_to_member_id: NotRequired[uuid.UUID | None]
    settlement_tx_id: NotRequired[uuid.UUID | None]
    meta: NotRequired[dict]