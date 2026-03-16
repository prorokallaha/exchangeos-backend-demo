from __future__ import annotations

import uuid

from app.db.gateway import DBGateway
from app.db.models.enums import AuditAction, RequisiteKind
from app.db.models.payment_requisite import PaymentRequisite
from app.services.bootstrap.audit_service import create_audit_log


async def create_payment_requisite(
    gw: DBGateway,
    *,
    organization_id: uuid.UUID,
    kind: RequisiteKind,
    label: str,
    currency: str,
    details: dict,
    limits: dict,
    created_by_member_id: uuid.UUID,
) -> PaymentRequisite:
    repo = gw.payment_requisites()

    created = await repo.create(
        {
            "organization_id": organization_id,
            "kind": kind,
            "label": label,
            "currency": currency,
            "details": details,
            "limits": limits,
            "is_active": True,
            "created_by_member_id": created_by_member_id,
        }
    )
    if not created:
        raise RuntimeError("Failed to create payment requisite")

    await create_audit_log(
        gw=gw,
        action=AuditAction.CREATE,
        entity_type="payment_requisite",
        entity_id=created.id,
        organization_id=organization_id,
        actor_member_id=created_by_member_id,
        data={
            "kind": created.kind.value,
            "label": created.label,
            "currency": created.currency,
        },
    )

    return created


async def update_payment_requisite(
    gw: DBGateway,
    *,
    organization_id: uuid.UUID,
    requisite_id: uuid.UUID,
    updated_by_member_id: uuid.UUID,
    label: str | None = None,
    details: dict | None = None,
    limits: dict | None = None,
    is_active: bool | None = None,
) -> PaymentRequisite:
    repo = gw.payment_requisites()

    requisite = await repo.get_by_id(requisite_id)
    if not requisite:
        raise ValueError("Payment requisite not found")

    if requisite.organization_id != organization_id:
        raise ValueError("Payment requisite does not belong to this organization")

    update_data: dict = {}

    if label is not None:
        update_data["label"] = label
    if details is not None:
        update_data["details"] = details
    if limits is not None:
        update_data["limits"] = limits
    if is_active is not None:
        update_data["is_active"] = is_active

    if not update_data:
        raise ValueError("No update fields provided")

    updated = await repo.update(requisite_id, update_data)
    if not updated:
        raise RuntimeError("Failed to update payment requisite")

    await create_audit_log(
        gw=gw,
        action=AuditAction.UPDATE,
        entity_type="payment_requisite",
        entity_id=updated.id,
        organization_id=organization_id,
        actor_member_id=updated_by_member_id,
        data=update_data,
    )

    return updated