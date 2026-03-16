from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.access import get_current_member
from app.api.deps.auth import get_current_user
from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.organization import OrganizationOut

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)


@router.get("/{organization_id}", response_model=OrganizationOut)
async def get_organization(
    organization_id: UUID,
    _: object = Depends(get_current_member),
    gw: DBGateway = Depends(get_gateway),
) -> OrganizationOut:
    organization = await gw.organizations().get_by_id(organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="organization not found",
        )

    return OrganizationOut(
        id=organization.id,
        name=organization.name,
    )

@router.get("/{organization_id}/me")
async def get_my_organization_context(
    organization_id: UUID,
    current_user=Depends(get_current_user),
    current_member=Depends(get_current_member),
):
    return {
        "organization_id": str(organization_id),
        "user": {
            "id": str(current_user.id),
            "login": current_user.login,
            "display_name": current_user.display_name,
            "is_platform_admin": current_user.is_platform_admin,
        },
        "member": {
            "id": str(current_member.id),
            "organization_id": str(current_member.organization_id),
            "user_id": str(current_member.user_id),
            "role_id": str(current_member.role_id),
            "role_type": current_member.role_type.value if hasattr(current_member.role_type, "value") else str(current_member.role_type),
            "status": current_member.status.value if hasattr(current_member.status, "value") else str(current_member.status),
        },
    }

@router.get("/{organization_id}/roles")
async def list_organization_roles(
    organization_id: UUID,
    _: object = Depends(get_current_member),
    gw: DBGateway = Depends(get_gateway),
):
    roles = await gw.roles().list_by_org(organization_id)

    return [
        {
            "id": str(role.id),
            "organization_id": str(role.organization_id),
            "name": role.name,
            "is_system": role.is_system,
        }
        for role in roles
    ]