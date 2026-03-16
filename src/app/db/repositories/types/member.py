from __future__ import annotations
from typing import NotRequired, TypedDict
import uuid

from app.db.models.enums import MemberStatus, RoleType


class MemberCreate(TypedDict):
    organization_id: uuid.UUID
    user_id: uuid.UUID
    role_type: RoleType
    role_id: NotRequired[uuid.UUID | None]
    created_by_member_id: NotRequired[uuid.UUID | None]


class MemberUpdate(TypedDict, total=False):
    status: NotRequired[MemberStatus]
    role_type: NotRequired[RoleType]
    role_id: NotRequired[uuid.UUID | None]