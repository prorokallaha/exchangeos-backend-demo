from __future__ import annotations

import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import PermissionEffect


class MemberPermission(Base):
    __tablename__ = "member_permissions"

    member_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organization_members.id"), primary_key=True)
    permission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("permissions.id"), primary_key=True)

    effect: Mapped[PermissionEffect] = mapped_column(
        Enum(PermissionEffect, name="permission_effect"),
        nullable=False,
        default=PermissionEffect.ALLOW,
    )

    member: Mapped["OrganizationMember"] = relationship(back_populates="permission_overrides")
    permission: Mapped["Permission"] = relationship(back_populates="member_links")