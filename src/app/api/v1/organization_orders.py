from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.access import get_current_member
from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.order import OrderAssignIn, OrderCreateIn, OrderOut, OrderUpdateIn
from app.services.access.access_service import has_permission
from app.services.orders_service import create_order, update_order

router = APIRouter(
    prefix="/organizations/{organization_id}/orders",
    tags=["organization-orders"],
)


@router.get("", response_model=list[OrderOut])
async def list_organization_orders(
    organization_id: UUID,
    current_member=Depends(get_current_member),
    gw: DBGateway = Depends(get_gateway),
) -> list[OrderOut]:
    can_read_all = await has_permission(
        gw,
        member_id=current_member.id,
        permission_code="orders.read_all",
    )

    if can_read_all:
        orders = await gw.orders().list_by_org(organization_id)
    else:
        can_read_own = await has_permission(
            gw,
            member_id=current_member.id,
            permission_code="orders.read_own",
        )
        if not can_read_own:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="missing permission: orders.read_own",
            )
        orders = await gw.orders().list_by_creator(current_member.id)

    return [
        OrderOut(
            id=order.id,
            organization_id=order.organization_id,
            type=order.type,
            status=order.status,
            amount_in=order.amount_in,
            currency_in=order.currency_in,
            amount_out=order.amount_out,
            currency_out=order.currency_out,
            rate=order.rate,
            created_by_member_id=order.created_by_member_id,
            assigned_to_member_id=order.assigned_to_member_id,
            settlement_tx_id=order.settlement_tx_id,
            meta=order.meta,
        )
        for order in orders
    ]


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_organization_order(
    organization_id: UUID,
    payload: OrderCreateIn,
    current_member=Depends(get_current_member),
    gw: DBGateway = Depends(get_gateway),
) -> OrderOut:
    can_create = await has_permission(
        gw,
        member_id=current_member.id,
        permission_code="orders.create",
    )
    if not can_create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="missing permission: orders.create",
        )

    try:
        order = await create_order(
            gw=gw,
            organization_id=organization_id,
            created_by_member_id=current_member.id,
            order_type=payload.type,
            amount_in=payload.amount_in,
            currency_in=payload.currency_in,
            amount_out=payload.amount_out,
            currency_out=payload.currency_out,
            rate=payload.rate,
            meta=payload.meta,
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

    return OrderOut(
        id=order.id,
        organization_id=order.organization_id,
        type=order.type,
        status=order.status,
        amount_in=order.amount_in,
        currency_in=order.currency_in,
        amount_out=order.amount_out,
        currency_out=order.currency_out,
        rate=order.rate,
        created_by_member_id=order.created_by_member_id,
        assigned_to_member_id=order.assigned_to_member_id,
        settlement_tx_id=order.settlement_tx_id,
        meta=order.meta,
    )


@router.get("/{order_id}", response_model=OrderOut)
async def get_organization_order(
    organization_id: UUID,
    order_id: UUID,
    current_member=Depends(get_current_member),
    gw: DBGateway = Depends(get_gateway),
) -> OrderOut:
    order = await gw.orders().get_by_id(order_id)
    if not order or order.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="order not found",
        )

    can_read_all = await has_permission(
        gw,
        member_id=current_member.id,
        permission_code="orders.read_all",
    )
    if not can_read_all:
        can_read_own = await has_permission(
            gw,
            member_id=current_member.id,
            permission_code="orders.read_own",
        )
        if not can_read_own or order.created_by_member_id != current_member.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="missing permission to read this order",
            )

    return OrderOut(
        id=order.id,
        organization_id=order.organization_id,
        type=order.type,
        status=order.status,
        amount_in=order.amount_in,
        currency_in=order.currency_in,
        amount_out=order.amount_out,
        currency_out=order.currency_out,
        rate=order.rate,
        created_by_member_id=order.created_by_member_id,
        assigned_to_member_id=order.assigned_to_member_id,
        settlement_tx_id=order.settlement_tx_id,
        meta=order.meta,
    )


@router.patch("/{order_id}", response_model=OrderOut)
async def patch_organization_order(
    organization_id: UUID,
    order_id: UUID,
    payload: OrderUpdateIn,
    current_member=Depends(get_current_member),
    gw: DBGateway = Depends(get_gateway),
) -> OrderOut:
    order = await gw.orders().get_by_id(order_id)
    if not order or order.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="order not found",
        )

    can_update_all = await has_permission(
        gw,
        member_id=current_member.id,
        permission_code="orders.update_all",
    )

    if not can_update_all:
        can_update_own = await has_permission(
            gw,
            member_id=current_member.id,
            permission_code="orders.update_own",
        )
        if not can_update_own or order.created_by_member_id != current_member.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="missing permission to update this order",
            )

    try:
        updated = await update_order(
            gw=gw,
            organization_id=organization_id,
            order_id=order_id,
            updated_by_member_id=current_member.id,
            status=payload.status,
            assigned_to_member_id=payload.assigned_to_member_id,
            meta=payload.meta,
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

    return OrderOut(
        id=updated.id,
        organization_id=updated.organization_id,
        type=updated.type,
        status=updated.status,
        amount_in=updated.amount_in,
        currency_in=updated.currency_in,
        amount_out=updated.amount_out,
        currency_out=updated.currency_out,
        rate=updated.rate,
        created_by_member_id=updated.created_by_member_id,
        assigned_to_member_id=updated.assigned_to_member_id,
        settlement_tx_id=updated.settlement_tx_id,
        meta=updated.meta,
    )


@router.post("/{order_id}/assign", response_model=OrderOut)
async def assign_organization_order(
    organization_id: UUID,
    order_id: UUID,
    payload: OrderAssignIn,
    current_member=Depends(get_current_member),
    gw: DBGateway = Depends(get_gateway),
) -> OrderOut:
    order = await gw.orders().get_by_id(order_id)
    if not order or order.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="order not found",
        )

    can_update_all = await has_permission(
        gw,
        member_id=current_member.id,
        permission_code="orders.update_all",
    )
    if not can_update_all:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="missing permission: orders.update_all",
        )

    try:
        updated = await update_order(
            gw=gw,
            organization_id=organization_id,
            order_id=order_id,
            updated_by_member_id=current_member.id,
            assigned_to_member_id=payload.assigned_to_member_id,
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

    return OrderOut(
        id=updated.id,
        organization_id=updated.organization_id,
        type=updated.type,
        status=updated.status,
        amount_in=updated.amount_in,
        currency_in=updated.currency_in,
        amount_out=updated.amount_out,
        currency_out=updated.currency_out,
        rate=updated.rate,
        created_by_member_id=updated.created_by_member_id,
        assigned_to_member_id=updated.assigned_to_member_id,
        settlement_tx_id=updated.settlement_tx_id,
        meta=updated.meta,
    )