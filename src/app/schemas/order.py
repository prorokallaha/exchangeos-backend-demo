from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.db.models.enums import OrderStatus, OrderType


class OrderCreateIn(BaseModel):
    type: OrderType
    amount_in: Decimal
    currency_in: str
    amount_out: Decimal
    currency_out: str
    rate: Decimal
    meta: dict | None = None


class OrderUpdateIn(BaseModel):
    status: OrderStatus | None = None
    assigned_to_member_id: UUID | None = None
    meta: dict | None = None


class OrderAssignIn(BaseModel):
    assigned_to_member_id: UUID


class OrderOut(BaseModel):
    id: UUID
    organization_id: UUID
    type: OrderType
    status: OrderStatus
    amount_in: Decimal
    currency_in: str
    amount_out: Decimal
    currency_out: str
    rate: Decimal
    created_by_member_id: UUID | None
    assigned_to_member_id: UUID | None
    settlement_tx_id: UUID | None
    meta: dict