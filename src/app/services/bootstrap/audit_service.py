from __future__ import annotations

import uuid

from app.db.gateway import DBGateway
from app.db.models.enums import AuditAction


async def create_audit_log(
    gw: DBGateway,
    action: AuditAction,
    entity_type: str,
    data: dict,
    organization_id: uuid.UUID | None = None,
    actor_member_id: uuid.UUID | None = None,
    entity_id: uuid.UUID | None = None,
) -> None:
    await gw.audit_logs().create(
        {
            "organization_id": organization_id,
            "actor_member_id": actor_member_id,
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": data,
        }
    )