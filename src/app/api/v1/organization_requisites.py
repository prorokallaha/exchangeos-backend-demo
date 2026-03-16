from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.access import require_org_permission
from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.payment_requisite import (
    PaymentRequisiteCreateIn,
    PaymentRequisiteOut,
    PaymentRequisiteUpdateIn,
)
from app.services.requisites_service import (
    create_payment_requisite,
    update_payment_requisite,
)

router = APIRouter(
    prefix="/organizations/{organization_id}/requisites",
    tags=["organization-requisites"],
)


@router.get("", response_model=list[PaymentRequisiteOut])
async def list_organization_requisites(
    organization_id: UUID,
    _: object = Depends(require_org_permission("requisites.read")),
    gw: DBGateway = Depends(get_gateway),
) -> list[PaymentRequisiteOut]:
    requisites = await gw.payment_requisites().list_by_org(organization_id)

    return [
        PaymentRequisiteOut(
            id=requisite.id,
            organization_id=requisite.organization_id,
            kind=requisite.kind,
            label=requisite.label,
            currency=requisite.currency,
            details=requisite.details,
            limits=requisite.limits,
            is_active=requisite.is_active,
            created_by_member_id=requisite.created_by_member_id,
        )
        for requisite in requisites
    ]


@router.post("", response_model=PaymentRequisiteOut, status_code=status.HTTP_201_CREATED)
async def create_organization_requisite(
    organization_id: UUID,
    payload: PaymentRequisiteCreateIn,
    current_member=Depends(require_org_permission("requisites.manage")),
    gw: DBGateway = Depends(get_gateway),
) -> PaymentRequisiteOut:
    try:
        requisite = await create_payment_requisite(
            gw=gw,
            organization_id=organization_id,
            kind=payload.kind,
            label=payload.label,
            currency=payload.currency,
            details=payload.details,
            limits=payload.limits,
            created_by_member_id=current_member.id,
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return PaymentRequisiteOut(
        id=requisite.id,
        organization_id=requisite.organization_id,
        kind=requisite.kind,
        label=requisite.label,
        currency=requisite.currency,
        details=requisite.details,
        limits=requisite.limits,
        is_active=requisite.is_active,
        created_by_member_id=requisite.created_by_member_id,
    )


@router.patch("/{requisite_id}", response_model=PaymentRequisiteOut)
async def patch_organization_requisite(
    organization_id: UUID,
    requisite_id: UUID,
    payload: PaymentRequisiteUpdateIn,
    current_member=Depends(require_org_permission("requisites.manage")),
    gw: DBGateway = Depends(get_gateway),
) -> PaymentRequisiteOut:
    try:
        requisite = await update_payment_requisite(
            gw=gw,
            organization_id=organization_id,
            requisite_id=requisite_id,
            updated_by_member_id=current_member.id,
            label=payload.label,
            details=payload.details,
            limits=payload.limits,
            is_active=payload.is_active,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return PaymentRequisiteOut(
        id=requisite.id,
        organization_id=requisite.organization_id,
        kind=requisite.kind,
        label=requisite.label,
        currency=requisite.currency,
        details=requisite.details,
        limits=requisite.limits,
        is_active=requisite.is_active,
        created_by_member_id=requisite.created_by_member_id,
    )