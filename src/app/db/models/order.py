from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import OrderStatus, OrderType
from app.db.models.mixins import TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)

    type: Mapped[OrderType] = mapped_column(Enum(OrderType, name="order_type"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.NEW)

    amount_in: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    currency_in: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    amount_out: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    currency_out: Mapped[str] = mapped_column(String(16), nullable=False, index=True)

    rate: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)

    created_by_member_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organization_members.id"), nullable=True)
    assigned_to_member_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organization_members.id"), nullable=True)

    settlement_tx_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ledger_transactions.id"), nullable=True)

    meta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    settlement_tx: Mapped["LedgerTransaction | None"] = relationship(back_populates="order")