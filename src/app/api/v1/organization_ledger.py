from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.access import require_org_permission
from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.ledger import LedgerEntryOut, LedgerTransactionOut

router = APIRouter(
    prefix="/organizations/{organization_id}/ledger",
    tags=["organization-ledger"],
)


@router.get("/transactions", response_model=list[LedgerTransactionOut])
async def list_ledger_transactions(
    organization_id: UUID,
    _: object = Depends(require_org_permission("ledger.read")),
    gw: DBGateway = Depends(get_gateway),
) -> list[LedgerTransactionOut]:
    txs = await gw.ledger_transactions().list_by_org(organization_id)

    return [
        LedgerTransactionOut(
            id=tx.id,
            organization_id=tx.organization_id,
            type=tx.type,
            status=tx.status,
            created_by_member_id=tx.created_by_member_id,
        )
        for tx in txs
    ]


@router.get("/transactions/{tx_id}", response_model=LedgerTransactionOut)
async def get_ledger_transaction(
    organization_id: UUID,
    tx_id: UUID,
    _: object = Depends(require_org_permission("ledger.read")),
    gw: DBGateway = Depends(get_gateway),
) -> LedgerTransactionOut:
    tx = await gw.ledger_transactions().get_by_id(tx_id)
    if not tx or tx.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ledger transaction not found",
        )

    return LedgerTransactionOut(
        id=tx.id,
        organization_id=tx.organization_id,
        type=tx.type,
        status=tx.status,
        created_by_member_id=tx.created_by_member_id,
    )


@router.get("/transactions/{tx_id}/entries", response_model=list[LedgerEntryOut])
async def list_ledger_transaction_entries(
    organization_id: UUID,
    tx_id: UUID,
    _: object = Depends(require_org_permission("ledger.read")),
    gw: DBGateway = Depends(get_gateway),
) -> list[LedgerEntryOut]:
    tx = await gw.ledger_transactions().get_by_id(tx_id)
    if not tx or tx.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ledger transaction not found",
        )

    entries = await gw.ledger_entries().list_by_transaction(tx_id)

    return [
        LedgerEntryOut(
            id=entry.id,
            organization_id=entry.organization_id,
            transaction_id=entry.transaction_id,
            account_id=entry.account_id,
            direction=entry.direction,
            amount=entry.amount,
            currency=entry.currency,
            description=entry.description,
        )
        for entry in entries
    ]