from __future__ import annotations

from typing import TypedDict
import uuid


class RolePermissionCreate(TypedDict):
    role_id: uuid.UUID
    permission_id: uuid.UUID