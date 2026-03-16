from __future__ import annotations

import uuid

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.enums import MemberStatus, RoleType
from app.db.models.mixins import TimestampMixin


class OrganizationMember(Base, TimestampMixin):
    __tablename__ = "organization_members"
    __table_args__ = (
        UniqueConstraint("organization_id", "user_id", name="uq_org_member_user"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    status: Mapped[MemberStatus] = mapped_column(Enum(MemberStatus, name="member_status"), nullable=False, default=MemberStatus.ACTIVE)

    # Базовая роль типа owner/manager/operator/viewer.
    # Мы храним и role_type (быстро) и role_id (гибко), чтобы можно было иметь кастомные роли.
    role_type: Mapped[RoleType] = mapped_column(Enum(RoleType, name="role_type"), nullable=False, default=RoleType.OPERATOR)
    role_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=True)

    created_by_member_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("organization_members.id"), nullable=True)

    organization: Mapped["Organization"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="members")

    role: Mapped["Role | None"] = relationship(back_populates="members")

    permission_overrides: Mapped[list["MemberPermission"]] = relationship(back_populates="member")