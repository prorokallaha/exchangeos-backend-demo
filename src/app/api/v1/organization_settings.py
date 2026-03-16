from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps.access import require_org_permission
from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.organization_setting import (
    OrganizationSettingOut,
    OrganizationSettingUpdateIn,
)
from app.services.bootstrap.settings_service import update_org_setting

router = APIRouter(
    prefix="/organizations/{organization_id}/settings",
    tags=["organization-settings"],
)


@router.get("", response_model=list[OrganizationSettingOut])
async def list_organization_settings(
    organization_id: UUID,
    _: object = Depends(require_org_permission("org.settings.manage")),
    gw: DBGateway = Depends(get_gateway),
) -> list[OrganizationSettingOut]:
    settings = await gw.organization_settings().list_by_org(organization_id)

    return [
        OrganizationSettingOut(
            id=setting.id,
            organization_id=setting.organization_id,
            key=setting.key,
            value=setting.value,
        )
        for setting in settings
    ]


@router.patch("/{key}", response_model=OrganizationSettingOut)
async def patch_organization_setting(
    organization_id: UUID,
    key: str,
    payload: OrganizationSettingUpdateIn,
    current_member=Depends(require_org_permission("org.settings.manage")),
    gw: DBGateway = Depends(get_gateway),
) -> OrganizationSettingOut:
    try:
        setting = await update_org_setting(
            gw=gw,
            organization_id=organization_id,
            key=key,
            value=payload.value,
            updated_by_member_id=current_member.id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return OrganizationSettingOut(
        id=setting.id,
        organization_id=setting.organization_id,
        key=setting.key,
        value=setting.value,
    )