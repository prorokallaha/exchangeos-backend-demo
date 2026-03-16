from __future__ import annotations

from typing import NotRequired, TypedDict
import uuid


class RoleCreate(TypedDict):
    organization_id: uuid.UUID
    name: str
    is_system: bool


class RoleUpdate(TypedDict, total=False):
    name: NotRequired[str]
    is_system: NotRequired[bool]