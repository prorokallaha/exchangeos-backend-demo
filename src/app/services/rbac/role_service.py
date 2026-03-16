from __future__ import annotations

import uuid

from app.db.gateway import DBGateway
from app.db.models.enums import RoleType
from app.db.models.role import Role
from app.services.rbac.constants import ROLE_PERMISSIONS


async def ensure_system_role(
    gw: DBGateway,
    organization_id: uuid.UUID,
    role_type: RoleType,
) -> Role:
    roles_repo = gw.roles()

    role_name = role_type.value.capitalize()
    existing = await roles_repo.get_by_name(organization_id, role_name)
    if existing:
        return existing

    created = await roles_repo.create(
        {
            "organization_id": organization_id,
            "name": role_name,
            "is_system": True,
        }
    )
    if not created:
        raise RuntimeError(f"Failed to create system role: {role_name}")

    return created


async def attach_permissions_to_role(
    gw: DBGateway,
    role_id: uuid.UUID,
    permission_codes: list[str],
) -> None:
    permissions_repo = gw.permissions()
    role_permissions_repo = gw.role_permissions()

    for code in permission_codes:
        permission = await permissions_repo.get_by_code(code)
        if not permission:
            raise RuntimeError(f"Permission not found: {code}")

        exists = await role_permissions_repo.exists_link(role_id, permission.id)
        if exists:
            continue

        await role_permissions_repo.create(
            {
                "role_id": role_id,
                "permission_id": permission.id,
            }
        )


async def seed_system_roles_for_org(
    gw: DBGateway,
    organization_id: uuid.UUID,
) -> dict[RoleType, Role]:
    result: dict[RoleType, Role] = {}

    for role_type in RoleType:
        role = await ensure_system_role(
            gw=gw,
            organization_id=organization_id,
            role_type=role_type,
        )
        await attach_permissions_to_role(
            gw=gw,
            role_id=role.id,
            permission_codes=ROLE_PERMISSIONS[role_type],
        )
        result[role_type] = role

    return result