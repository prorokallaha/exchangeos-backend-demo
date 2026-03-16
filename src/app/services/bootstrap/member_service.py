from __future__ import annotations

import uuid

from app.db.gateway import DBGateway
from app.db.models.enums import AuditAction, MemberStatus, RoleType
from app.db.models.organization_member import OrganizationMember
from app.db.models.user import User
from app.services.bootstrap.audit_service import create_audit_log


async def create_member_user(
    gw: DBGateway,
    *,
    organization_id: uuid.UUID,
    created_by_member_id: uuid.UUID,
    login: str,
    display_name: str,
    password_hash: str,
    role_type: RoleType,
) -> tuple[User, OrganizationMember]:
    users_repo = gw.users()
    members_repo = gw.members()
    roles_repo = gw.roles()

    existing_user = await users_repo.get_by_login(login)
    if existing_user:
        raise ValueError(f"User with login '{login}' already exists")

    role = await roles_repo.get_by_name(organization_id, role_type.value.capitalize())
    if not role:
        raise RuntimeError(f"System role not found for role type: {role_type.value}")

    user = await users_repo.create(
        {
            "login": login,
            "display_name": display_name,
            "password_hash": password_hash,
            "is_platform_admin": False,
        }
    )
    if not user:
        raise RuntimeError("Failed to create member user")

    member = await members_repo.create(
        {
            "organization_id": organization_id,
            "user_id": user.id,
            "role_type": role_type,
            "role_id": role.id,
            "created_by_member_id": created_by_member_id,
        }
    )
    if not member:
        raise RuntimeError("Failed to create organization member")

    await create_audit_log(
        gw=gw,
        action=AuditAction.CREATE,
        entity_type="organization_member",
        entity_id=member.id,
        organization_id=organization_id,
        actor_member_id=created_by_member_id,
        data={
            "login": login,
            "display_name": display_name,
            "role_type": role_type.value,
        },
    )

    return user, member

async def update_member(
    gw: DBGateway,
    *,
    organization_id: uuid.UUID,
    member_id: uuid.UUID,
    updated_by_member_id: uuid.UUID,
    role_type: RoleType | None = None,
    status: MemberStatus | None = None,
) -> OrganizationMember:
    members_repo = gw.members()
    roles_repo = gw.roles()

    member = await members_repo.get_by_id(member_id)
    if not member:
        raise ValueError("Member not found")

    if member.organization_id != organization_id:
        raise ValueError("Member does not belong to this organization")

    update_data: dict = {}

    if role_type is not None:
        role = await roles_repo.get_by_name(organization_id, role_type.value)
        if not role:
            raise ValueError(f"Role '{role_type.value}' not found")

        update_data["role_type"] = role_type
        update_data["role_id"] = role.id

    if status is not None:
        update_data["status"] = status

    if not update_data:
        raise ValueError("No update fields provided")

    updated = await members_repo.update(member_id, update_data)
    if not updated:
        raise RuntimeError("Failed to update member")

    await create_audit_log(
        gw=gw,
        action=AuditAction.UPDATE,
        entity_type="organization_member",
        entity_id=updated.id,
        organization_id=organization_id,
        actor_member_id=updated_by_member_id,
        data={
            "role_type": update_data.get("role_type").value if update_data.get("role_type") else None,
            "status": update_data.get("status").value if update_data.get("status") else None,
        },
    )

    return updated