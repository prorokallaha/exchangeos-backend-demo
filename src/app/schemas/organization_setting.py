from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class OrganizationSettingOut(BaseModel):
    id: UUID
    organization_id: UUID
    key: str
    value: dict


class OrganizationSettingUpdateIn(BaseModel):
    value: dict