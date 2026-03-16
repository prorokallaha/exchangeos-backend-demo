from __future__ import annotations

import uuid

from app.db.gateway import DBGateway
from app.db.models.enums import AuditAction
from app.db.models.organization_setting import OrganizationSetting
from app.services.bootstrap.audit_service import create_audit_log

DEFAULT_ORG_SETTINGS: list[tuple[str, dict]] = [
    ("price_deviation_buy_bps", {"value": 0}),
    ("price_deviation_sell_bps", {"value": 0}),
    ("feed_mode", {"value": "default"}),
]


async def ensure_default_org_settings(
    gw: DBGateway,
    organization_id: uuid.UUID,
    updated_by_member_id: uuid.UUID | None = None,
) -> None:
    repo = gw.organization_settings()

    for key, value in DEFAULT_ORG_SETTINGS:
        existing = await repo.get_by_key(organization_id, key)
        if existing:
            continue

        await repo.create(
            {
                "organization_id": organization_id,
                "key": key,
                "value": value,
                "updated_by_member_id": updated_by_member_id,
            }
        )


async def update_org_setting(
    gw: DBGateway,
    *,
    organization_id: uuid.UUID,
    key: str,
    value: dict,
    updated_by_member_id: uuid.UUID,
) -> OrganizationSetting:
    repo = gw.organization_settings()

    existing = await repo.get_by_key(organization_id, key)
    if not existing:
        raise ValueError(f"Organization setting '{key}' not found")

    updated = await repo.update(
        existing.id,
        {
            "value": value,
            "updated_by_member_id": updated_by_member_id,
        },
    )
    if not updated:
        raise RuntimeError("Failed to update organization setting")

    await create_audit_log(
        gw=gw,
        action=AuditAction.UPDATE,
        entity_type="organization_setting",
        entity_id=updated.id,
        organization_id=organization_id,
        actor_member_id=updated_by_member_id,
        data={
            "key": key,
            "value": value,
        },
    )

    return updated