from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.db.models.enums import OrderType


class OrganizationStatsSummaryOut(BaseModel):
    total_orders: int
    completed_orders: int
    active_orders: int
    cancelled_orders: int
    total_volume_in: Decimal
    total_volume_out: Decimal


class OrganizationStatsByOrderTypeOut(BaseModel):
    type: OrderType
    count: int


class OrganizationStatsByCurrencyOut(BaseModel):
    currency: str
    count: int
    volume: Decimal


class OrganizationStatsByOperatorOut(BaseModel):
    member_id: UUID
    user_id: UUID | None
    login: str | None
    display_name: str | None
    orders_count: int
    completed_orders: int
    volume_in: Decimal
    volume_out: Decimal


class OrganizationStatsPeriodOut(BaseModel):
    period: str
    date_from: datetime | None
    date_to: datetime | None


class OrganizationStatsOut(BaseModel):
    period: OrganizationStatsPeriodOut
    summary: OrganizationStatsSummaryOut
    by_order_type: list[OrganizationStatsByOrderTypeOut]
    by_currency_in: list[OrganizationStatsByCurrencyOut]
    by_currency_out: list[OrganizationStatsByCurrencyOut]
    by_operator: list[OrganizationStatsByOperatorOut]