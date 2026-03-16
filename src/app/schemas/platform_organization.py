from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PlatformOrganizationCreateIn(BaseModel):
    organization_name: str = Field(min_length=1, max_length=255)
    owner_login: str = Field(min_length=3, max_length=64)
    owner_display_name: str = Field(min_length=1, max_length=128)
    owner_password_hash: str = Field(min_length=1, max_length=255)


class PlatformOrganizationCreateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    organization_id: UUID
    owner_user_id: UUID
    owner_member_id: UUID


class PlatformOrganizationByUserOut(BaseModel):
    organization_id: UUID
    organization_name: str
    member_id: UUID
    role_id: UUID
    role_type: str
    status: str