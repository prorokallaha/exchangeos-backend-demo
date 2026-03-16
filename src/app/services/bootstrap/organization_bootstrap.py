from __future__ import annotations

import uuid

from app.db.gateway import DBGateway
from app.db.models.enums import AuditAction, RoleType
from app.db.models.organization import Organization
from app.db.models.organization_member import OrganizationMember
from app.db.models.user import User
from app.services.bootstrap.account_service import ensure_default_accounts
from app.services.bootstrap.audit_service import create_audit_log
from app.services.bootstrap.settings_service import ensure_default_org_settings
from app.services.rbac.permission_service import seed_permissions
from app.services.rbac.role_service import seed_system_roles_for_org


class OrganizationBootstrapResult:
    def __init__(
        self,
        organization: Organization,
        owner_user: User,
        owner_member: OrganizationMember,
    ) -> None:
        self.organization = organization
        self.owner_user = owner_user
        self.owner_member = owner_member


async def create_organization_with_owner(
    gw: DBGateway,
    *,
    organization_name: str,
    owner_login: str,
    owner_display_name: str,
    owner_password_hash: str,
    created_by_platform_admin: bool = True,
) -> OrganizationBootstrapResult:
    users_repo = gw.users()
    organizations_repo = gw.organizations()
    members_repo = gw.members()

    existing_user = await users_repo.get_by_login(owner_login)
    if existing_user:
        raise ValueError(f"User with login '{owner_login}' already exists")

    organization = await organizations_repo.create(
        {
            "name": organization_name,
        }
    )
    if not organization:
        raise RuntimeError("Failed to create organization")

    owner_user = await users_repo.create(
        {
            "login": owner_login,
            "display_name": owner_display_name,
            "password_hash": owner_password_hash,
            "is_platform_admin": False,
        }
    )
    if not owner_user:
        raise RuntimeError("Failed to create owner user")

    await seed_permissions(gw)
    roles_map = await seed_system_roles_for_org(gw, organization.id)

    owner_role = roles_map[RoleType.OWNER]

    owner_member = await members_repo.create(
        {
            "organization_id": organization.id,
            "user_id": owner_user.id,
            "role_type": RoleType.OWNER,
            "role_id": owner_role.id,
            "created_by_member_id": None,
        }
    )
    if not owner_member:
        raise RuntimeError("Failed to create owner member")

    await ensure_default_org_settings(
        gw=gw,
        organization_id=organization.id,
        updated_by_member_id=owner_member.id,
    )
    await ensure_default_accounts(
        gw=gw,
        organization_id=organization.id,
    )

    await create_audit_log(
        gw=gw,
        action=AuditAction.CREATE,
        entity_type="organization",
        entity_id=organization.id,
        organization_id=organization.id,
        actor_member_id=None,
        data={
            "organization_name": organization.name,
            "owner_login": owner_user.login,
            "created_by_platform_admin": created_by_platform_admin,
        },
    )

    return OrganizationBootstrapResult(
        organization=organization,
        owner_user=owner_user,
        owner_member=owner_member,
    )