from __future__ import annotations

from uuid import UUID

from app.db.gateway import DBGateway
from app.db.models.enums import PermissionEffect
from app.services.exceptions import NotFoundError, PermissionDeniedError


async def get_member_for_user_in_org(
    gw: DBGateway,
    *,
    user_id: UUID,
    organization_id: UUID,
):
    """
    Return organization member for given user in given organization.
    """
    member = await gw.members().get_by_org_and_user(
        user_id=user_id,
        organization_id=organization_id,
    )
    if not member:
        raise NotFoundError("organization member not found")
    return member


async def get_effective_permission_codes(
    gw: DBGateway,
    *,
    member_id: UUID,
) -> set[str]:
    """
    Resolve effective permissions for member:
    1) role-based permissions
    2) member-level allow/deny overrides
    """
    member = await gw.members().get_by_id(member_id)
    if not member:
        raise NotFoundError("member not found")

    role = await gw.roles().get_by_id(member.role_id)
    if not role:
        raise NotFoundError("role not found")

    role_permissions = await gw.role_permissions().list_by_role(role.id)
    permission_ids = [rp.permission_id for rp in role_permissions]

    permissions: set[str] = set()

    if permission_ids:
        permission_rows = await gw.permissions().list_by_ids(permission_ids)
        permissions = {p.code for p in permission_rows}

    member_overrides = await gw.member_permissions().list_by_member(member.id)

    if member_overrides:
        override_permission_ids = [mp.permission_id for mp in member_overrides]
        override_permissions = await gw.permissions().list_by_ids(override_permission_ids)
        code_by_id = {p.id: p.code for p in override_permissions}

        for override in member_overrides:
            code = code_by_id.get(override.permission_id)
            if not code:
                continue

            if override.effect == PermissionEffect.ALLOW:
                permissions.add(code)
            elif override.effect == PermissionEffect.DENY:
                permissions.discard(code)

    return permissions


async def has_permission(
    gw: DBGateway,
    *,
    member_id: UUID,
    permission_code: str,
) -> bool:
    permissions = await get_effective_permission_codes(
        gw,
        member_id=member_id,
    )
    return permission_code in permissions


async def require_permission(
    gw: DBGateway,
    *,
    member_id: UUID,
    permission_code: str,
) -> None:
    allowed = await has_permission(
        gw,
        member_id=member_id,
        permission_code=permission_code,
    )
    if not allowed:
        raise PermissionDeniedError(
            f"missing permission: {permission_code}"
        )