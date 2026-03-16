from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.access import require_org_permission
from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.organization_member import (
    OrganizationMemberCreateIn,
    OrganizationMemberCreateOut,
    OrganizationMemberOut,
    OrganizationMemberUpdateIn,
)
from app.services.bootstrap.member_service import create_member_user, update_member

router = APIRouter(
    prefix="/organizations/{organization_id}/members",
    tags=["organization-members"],
)


@router.get("")
async def list_organization_members(
    organization_id: UUID,
    _: object = Depends(require_org_permission("org.members.manage")),
    gw: DBGateway = Depends(get_gateway),
):
    members = await gw.members().list_by_org(organization_id)

    return [
        {
            "id": str(member.id),
            "organization_id": str(member.organization_id),
            "user_id": str(member.user_id),
            "role_id": str(member.role_id),
            "role_type": member.role_type.value if hasattr(member.role_type, "value") else str(member.role_type),
            "status": member.status.value if hasattr(member.status, "value") else str(member.status),
        }
        for member in members
    ]


@router.post(
    "",
    response_model=OrganizationMemberCreateOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization_member(
    organization_id: UUID,
    payload: OrganizationMemberCreateIn,
    current_member=Depends(require_org_permission("org.members.manage")),
    gw: DBGateway = Depends(get_gateway),
) -> OrganizationMemberCreateOut:
    try:
        user, member = await create_member_user(
            gw=gw,
            organization_id=organization_id,
            login=payload.login,
            display_name=payload.display_name,
            password_hash=payload.password_hash,
            role_type=payload.role_type,
            created_by_member_id=current_member.id,
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

    return OrganizationMemberCreateOut(
        organization_id=organization_id,
        user_id=user.id,
        member_id=member.id,
        role_type=member.role_type,
    )


@router.patch(
    "/{member_id}",
    response_model=OrganizationMemberOut,
)
async def patch_organization_member(
    organization_id: UUID,
    member_id: UUID,
    payload: OrganizationMemberUpdateIn,
    current_member=Depends(require_org_permission("org.members.manage")),
    gw: DBGateway = Depends(get_gateway),
) -> OrganizationMemberOut:
    try:
        member = await update_member(
            gw=gw,
            organization_id=organization_id,
            member_id=member_id,
            updated_by_member_id=current_member.id,
            role_type=payload.role_type,
            status=payload.status,
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

    return OrganizationMemberOut(
        id=member.id,
        organization_id=member.organization_id,
        user_id=member.user_id,
        role_id=member.role_id,
        role_type=member.role_type,
        status=member.status,
    )