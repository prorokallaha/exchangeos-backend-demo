from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status

from app.api.deps.auth import get_current_user
from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.services.access.access_service import (
    get_member_for_user_in_org,
    require_permission,
)
from app.services.exceptions import NotFoundError, PermissionDeniedError


async def get_current_member(
    organization_id: UUID = Path(...),
    current_user=Depends(get_current_user),
    gw: DBGateway = Depends(get_gateway),
):
    try:
        member = await get_member_for_user_in_org(
            gw,
            user_id=current_user.id,
            organization_id=organization_id,
        )
        return member
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


def require_org_permission(permission_code: str) -> Callable:
    async def dependency(
        organization_id: UUID = Path(...),
        current_user=Depends(get_current_user),
        gw: DBGateway = Depends(get_gateway),
    ):
        try:
            member = await get_member_for_user_in_org(
                gw,
                user_id=current_user.id,
                organization_id=organization_id,
            )
            await require_permission(
                gw,
                member_id=member.id,
                permission_code=permission_code,
            )
            return member
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )
        except PermissionDeniedError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )

    return dependency