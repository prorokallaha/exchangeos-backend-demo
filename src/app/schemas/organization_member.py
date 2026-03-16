from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from app.db.models.enums import MemberStatus, RoleType


class OrganizationMemberCreateIn(BaseModel):
    login: str = Field(min_length=3, max_length=64)
    display_name: str = Field(min_length=1, max_length=128)
    password_hash: str = Field(min_length=1, max_length=255)
    role_type: RoleType


class OrganizationMemberCreateOut(BaseModel):
    organization_id: UUID
    user_id: UUID
    member_id: UUID
    role_type: RoleType


class OrganizationMemberUpdateIn(BaseModel):
    role_type: RoleType | None = None
    status: MemberStatus | None = None


class OrganizationMemberOut(BaseModel):
    id: UUID
    organization_id: UUID
    user_id: UUID
    role_id: UUID
    role_type: RoleType
    status: MemberStatus