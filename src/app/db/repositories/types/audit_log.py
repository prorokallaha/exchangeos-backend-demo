from __future__ import annotations

from typing import NotRequired, TypedDict
import uuid

from app.db.models.enums import AuditAction


class AuditLogCreate(TypedDict):
    action: AuditAction
    entity_type: str
    data: dict
    organization_id: NotRequired[uuid.UUID | None]
    actor_member_id: NotRequired[uuid.UUID | None]
    entity_id: NotRequired[uuid.UUID | None]