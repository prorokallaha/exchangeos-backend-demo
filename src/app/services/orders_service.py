from __future__ import annotations

import uuid
from decimal import Decimal

from app.db.gateway import DBGateway
from app.db.models.enums import AuditAction, OrderStatus, OrderType
from app.db.models.order import Order
from app.services.bootstrap.audit_service import create_audit_log
from app.services.order_rules import (
    validate_assignee,
    validate_order_creation_payload,
    validate_order_status_transition,
)
from app.services.settlement_service import create_order_settlement


async def create_order(
    gw: DBGateway,
    *,
    organization_id: uuid.UUID,
    created_by_member_id: uuid.UUID,
    order_type: OrderType,
    amount_in: Decimal,
    currency_in: str,
    amount_out: Decimal,
    currency_out: str,
    rate: Decimal,
    meta: dict | None = None,
) -> Order:
    repo = gw.orders()

    validate_order_creation_payload(
        amount_in=amount_in,
        currency_in=currency_in,
        amount_out=amount_out,
        currency_out=currency_out,
        rate=rate,
    )

    currency_in = currency_in.strip().upper()
    currency_out = currency_out.strip().upper()

    created = await repo.create(
        {
            "organization_id": organization_id,
            "type": order_type,
            "status": OrderStatus.NEW,
            "amount_in": amount_in,
            "currency_in": currency_in,
            "amount_out": amount_out,
            "currency_out": currency_out,
            "rate": rate,
            "created_by_member_id": created_by_member_id,
            "assigned_to_member_id": None,
            "settlement_tx_id": None,
            "meta": meta or {},
        }
    )
    if not created:
        raise RuntimeError("Failed to create order")

    await create_audit_log(
        gw=gw,
        action=AuditAction.CREATE,
        entity_type="order",
        entity_id=created.id,
        organization_id=organization_id,
        actor_member_id=created_by_member_id,
        data={
            "type": created.type.value,
            "status": created.status.value,
            "amount_in": str(created.amount_in),
            "currency_in": created.currency_in,
            "amount_out": str(created.amount_out),
            "currency_out": created.currency_out,
            "rate": str(created.rate),
        },
    )

    return created


async def update_order(
    gw: DBGateway,
    *,
    organization_id: uuid.UUID,
    order_id: uuid.UUID,
    updated_by_member_id: uuid.UUID,
    status: OrderStatus | None = None,
    assigned_to_member_id: uuid.UUID | None = None,
    meta: dict | None = None,
) -> Order:
    repo = gw.orders()

    order = await repo.get_by_id(order_id)
    if not order:
        raise ValueError("Order not found")

    if order.organization_id != organization_id:
        raise ValueError("Order does not belong to this organization")

    update_data: dict = {}

    if assigned_to_member_id is not None:
        assignee = await gw.members().get_by_id(assigned_to_member_id)
        if not assignee:
            raise ValueError("Assigned member not found")

        if assignee.organization_id != organization_id:
            raise ValueError("Assigned member does not belong to this organization")

        validate_assignee(assignee)
        update_data["assigned_to_member_id"] = assigned_to_member_id

    future_assignee_id = (
        assigned_to_member_id
        if assigned_to_member_id is not None
        else order.assigned_to_member_id
    )

    if status is not None:
        validate_order_status_transition(order.status, status)

        if status == OrderStatus.COMPLETED and future_assignee_id is None:
            raise ValueError("Cannot complete order without assigned operator")

        if status == OrderStatus.COMPLETED and order.settlement_tx_id is not None:
            raise ValueError("Order is already settled")

        update_data["status"] = status

    if meta is not None:
        update_data["meta"] = meta

    if status == OrderStatus.COMPLETED:
        settlement_tx = await create_order_settlement(
            gw=gw,
            order=order,
            actor_member_id=updated_by_member_id,
        )
        update_data["settlement_tx_id"] = settlement_tx.id

    if not update_data:
        raise ValueError("No update fields provided")

    updated = await repo.update(order_id, update_data)
    if not updated:
        raise RuntimeError("Failed to update order")

    await create_audit_log(
        gw=gw,
        action=AuditAction.UPDATE,
        entity_type="order",
        entity_id=updated.id,
        organization_id=organization_id,
        actor_member_id=updated_by_member_id,
        data={
            "status": update_data["status"].value if "status" in update_data else None,
            "assigned_to_member_id": (
                str(update_data["assigned_to_member_id"])
                if "assigned_to_member_id" in update_data
                else None
            ),
            "settlement_tx_id": (
                str(update_data["settlement_tx_id"])
                if "settlement_tx_id" in update_data
                else None
            ),
            "meta": update_data.get("meta"),
        },
    )

    return updated