from __future__ import annotations

import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import LedgerTxStatus, LedgerTxType
from app.db.models.mixins import TimestampMixin


class LedgerTransaction(Base, TimestampMixin):
    __tablename__ = "ledger_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)

    type: Mapped[LedgerTxType] = mapped_column(Enum(LedgerTxType, name="ledger_tx_type"), nullable=False)
    status: Mapped[LedgerTxStatus] = mapped_column(Enum(LedgerTxStatus, name="ledger_tx_status"), nullable=False, default=LedgerTxStatus.POSTED)

    created_by_member_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organization_members.id"), nullable=True)

    entries: Mapped[list["LedgerEntry"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")

    order: Mapped["Order | None"] = relationship(back_populates="settlement_tx", uselist=False)