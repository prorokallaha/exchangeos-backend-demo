from __future__ import annotations

from typing import NotRequired, TypedDict
import uuid


class OrganizationSettingCreate(TypedDict):
    organization_id: uuid.UUID
    key: str
    value: dict
    updated_by_member_id: NotRequired[uuid.UUID | None]


class OrganizationSettingUpdate(TypedDict, total=False):
    value: NotRequired[dict]
    updated_by_member_id: NotRequired[uuid.UUID | None]