from __future__ import annotations

from app.db.models.enums import RoleType

PERMISSIONS: list[tuple[str, str]] = [
    ("org.members.manage", "Manage organization members"),
    ("org.roles.manage", "Manage organization roles"),
    ("org.settings.manage", "Manage organization settings"),
    ("stats.org.read", "Read organization statistics"),
    ("orders.create", "Create orders"),
    ("orders.read_own", "Read own orders"),
    ("orders.read_all", "Read all organization orders"),
    ("orders.update_own", "Update own orders"),
    ("orders.update_all", "Update all organization orders"),
    ("requisites.read", "Read payment requisites"),
    ("requisites.manage", "Manage payment requisites"),
    ("ledger.read", "Read ledger data"),
]

ROLE_PERMISSIONS: dict[RoleType, list[str]] = {
    RoleType.OWNER: [
        "org.members.manage",
        "org.roles.manage",
        "org.settings.manage",
        "stats.org.read",
        "orders.create",
        "orders.read_all",
        "orders.update_all",
        "requisites.read",
        "requisites.manage",
        "ledger.read",
    ],
    RoleType.MANAGER: [
        "org.members.manage",
        "org.settings.manage",
        "stats.org.read",
        "orders.create",
        "orders.read_all",
        "orders.update_all",
        "requisites.read",
        "requisites.manage",
        "ledger.read",
    ],
    RoleType.OPERATOR: [
        "orders.create",
        "orders.read_own",
        "orders.update_own",
        "requisites.read",
    ],
    RoleType.VIEWER: [
        "orders.read_own",
        "requisites.read",
    ],
}