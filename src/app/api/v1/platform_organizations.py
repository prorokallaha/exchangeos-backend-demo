from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.platform_organization import (
    PlatformOrganizationByUserOut,
    PlatformOrganizationCreateIn,
    PlatformOrganizationCreateOut,
)
from app.services.bootstrap.organization_bootstrap import (
    create_organization_with_owner,
)

router = APIRouter(
    prefix="/platform/organizations",
    tags=["platform-organizations"],
)


@router.post(
    "",
    response_model=PlatformOrganizationCreateOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_platform_organization(
    payload: PlatformOrganizationCreateIn,
    gw: DBGateway = Depends(get_gateway),
) -> PlatformOrganizationCreateOut:
    try:
        result = await create_organization_with_owner(
            gw=gw,
            organization_name=payload.organization_name,
            owner_login=payload.owner_login,
            owner_display_name=payload.owner_display_name,
            owner_password_hash=payload.owner_password_hash,
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

    return PlatformOrganizationCreateOut(
        organization_id=result.organization.id,
        owner_user_id=result.owner_user.id,
        owner_member_id=result.owner_member.id,
    )


@router.get("/by-user/{user_id}", response_model=list[PlatformOrganizationByUserOut])
async def list_platform_organizations_by_user(
    user_id: UUID,
    gw: DBGateway = Depends(get_gateway),
) -> list[PlatformOrganizationByUserOut]:
    members = await gw.members().list_by_user(user_id)

    result: list[PlatformOrganizationByUserOut] = []

    for member in members:
        organization = await gw.organizations().get_by_id(member.organization_id)
        if not organization:
            continue

        result.append(
            PlatformOrganizationByUserOut(
                organization_id=organization.id,
                organization_name=organization.name,
                member_id=member.id,
                role_id=member.role_id,
                role_type=member.role_type.value,
                status=member.status.value,
            )
        )

    return result