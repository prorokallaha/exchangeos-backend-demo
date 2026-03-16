from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin


class OrganizationSetting(Base, TimestampMixin):
    __tablename__ = "organization_settings"
    __table_args__ = (UniqueConstraint("organization_id", "key", name="uq_org_setting_key"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    key: Mapped[str] = mapped_column(nullable=False, index=True)

    # храним значения как jsonb (поддержка int/bool/decimal/str/json – всё тут)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    updated_by_member_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organization_members.id"), nullable=True)

    organization: Mapped["Organization"] = relationship(back_populates="settings")