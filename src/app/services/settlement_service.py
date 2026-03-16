from __future__ import annotations

import uuid

from app.db.gateway import DBGateway
from app.db.models.enums import (
    AuditAction,
    EntryDirection,
    LedgerTxStatus,
    LedgerTxType,
)
from app.db.models.ledger_transaction import LedgerTransaction
from app.services.bootstrap.audit_service import create_audit_log


async def create_order_settlement(
    gw: DBGateway,
    *,
    order,
    actor_member_id: uuid.UUID | None,
) -> LedgerTransaction:
    if order.settlement_tx_id is not None:
        raise ValueError("Order already has settlement transaction")

    accounts_repo = gw.accounts()
    ledger_tx_repo = gw.ledger_transactions()
    ledger_entries_repo = gw.ledger_entries()

    account_in = await accounts_repo.get_internal_by_currency(
        order.organization_id,
        order.currency_in,
    )
    if not account_in:
        raise ValueError(
            f"Active internal account for currency '{order.currency_in}' not found"
        )

    account_out = await accounts_repo.get_internal_by_currency(
        order.organization_id,
        order.currency_out,
    )
    if not account_out:
        raise ValueError(
            f"Active internal account for currency '{order.currency_out}' not found"
        )

    tx = await ledger_tx_repo.create(
        {
            "organization_id": order.organization_id,
            "type": LedgerTxType.ORDER,
            "status": LedgerTxStatus.POSTED,
            "created_by_member_id": actor_member_id,
        }
    )
    if not tx:
        raise RuntimeError("Failed to create settlement transaction")

    entry_in = await ledger_entries_repo.create(
        {
            "organization_id": order.organization_id,
            "transaction_id": tx.id,
            "account_id": account_in.id,
            "direction": EntryDirection.DEBIT,
            "amount": order.amount_in,
            "currency": order.currency_in,
            "description": f"Order {order.id} settlement inflow",
        }
    )
    if not entry_in:
        raise RuntimeError("Failed to create settlement inflow entry")

    entry_out = await ledger_entries_repo.create(
        {
            "organization_id": order.organization_id,
            "transaction_id": tx.id,
            "account_id": account_out.id,
            "direction": EntryDirection.CREDIT,
            "amount": order.amount_out,
            "currency": order.currency_out,
            "description": f"Order {order.id} settlement outflow",
        }
    )
    if not entry_out:
        raise RuntimeError("Failed to create settlement outflow entry")

    await create_audit_log(
        gw=gw,
        action=AuditAction.CREATE,
        entity_type="ledger_transaction",
        entity_id=tx.id,
        organization_id=order.organization_id,
        actor_member_id=actor_member_id,
        data={
            "order_id": str(order.id),
            "type": tx.type.value,
            "status": tx.status.value,
            "currency_in": order.currency_in,
            "amount_in": str(order.amount_in),
            "currency_out": order.currency_out,
            "amount_out": str(order.amount_out),
            "account_in_id": str(account_in.id),
            "account_out_id": str(account_out.id),
        },
    )

    return tx